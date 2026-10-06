import os
import flet as ft
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def db():
    return mysql.connector.connect(host=os.getenv('DB_HOST','localhost'),port=int(os.getenv('DB_PORT','3306')),user=os.getenv('DB_USER','root'),password=os.getenv('DB_PASSWORD',''),database=os.getenv('DB_NAME','soporte_ti'))

def query(sql,args=(),fetch=True):
    c=db()
    try:
        cur=c.cursor(dictionary=True)
        cur.execute(sql,args)
        if fetch:
            return cur.fetchall()
        c.commit()
        return cur.lastrowid
    finally:
        c.close()

def main(page: ft.Page):
    page.title='MesaSimple TI'
    page.theme_mode=ft.ThemeMode.DARK
    page.padding=20
    selected_id=ft.Text(value='')
    titulo=ft.TextField(label='Título',expand=True)
    descripcion=ft.TextField(label='Descripción',multiline=True,min_lines=2,max_lines=4)
    prioridad=ft.Dropdown(label='Prioridad',options=[ft.dropdown.Option(x) for x in ['Baja','Media','Alta']],value='Media')
    estado=ft.Dropdown(label='Estado',options=[ft.dropdown.Option(x) for x in ['Abierto','En proceso','Resuelto']],value='Abierto')
    usuario=ft.Dropdown(label='Usuario')
    tecnico=ft.Dropdown(label='Técnico')
    buscar=ft.TextField(label='Buscar ticket',prefix_icon=ft.Icons.SEARCH,on_change=lambda e:cargar())
    lista=ft.Column(scroll=ft.ScrollMode.AUTO)
    resumen=ft.Row()

    def aviso(texto,error=False):
        page.snack_bar=ft.SnackBar(ft.Text(texto),bgcolor=ft.Colors.RED_700 if error else ft.Colors.GREEN_700)
        page.snack_bar.open=True
        page.update()

    def combos():
        usuario.options=[ft.dropdown.Option(str(x['id']),x['nombre']) for x in query('SELECT id,nombre FROM usuarios ORDER BY nombre')]
        tecnico.options=[ft.dropdown.Option('', 'Sin asignar')]+[ft.dropdown.Option(str(x['id']),x['nombre']) for x in query('SELECT id,nombre FROM tecnicos WHERE activo=1 ORDER BY nombre')]

    def limpiar(e=None):
        selected_id.value=''; titulo.value=''; descripcion.value=''; prioridad.value='Media'; estado.value='Abierto'; usuario.value=None; tecnico.value=''; page.update()

    def guardar(e):
        try:
            if not titulo.value.strip() or not descripcion.value.strip() or not usuario.value:
                aviso('Completa título, descripción y usuario',True); return
            tid=int(tecnico.value) if tecnico.value else None
            if selected_id.value:
                query('UPDATE tickets SET usuario_id=%s,tecnico_id=%s,titulo=%s,descripcion=%s,prioridad=%s,estado=%s WHERE id=%s',(int(usuario.value),tid,titulo.value.strip(),descripcion.value.strip(),prioridad.value,estado.value,int(selected_id.value)),False)
                aviso('Ticket actualizado')
            else:
                query('INSERT INTO tickets(usuario_id,tecnico_id,titulo,descripcion,prioridad,estado) VALUES(%s,%s,%s,%s,%s,%s)',(int(usuario.value),tid,titulo.value.strip(),descripcion.value.strip(),prioridad.value,estado.value),False)
                aviso('Ticket registrado')
            limpiar(); cargar()
        except Exception as ex: aviso(str(ex),True)

    def editar(t):
        selected_id.value=str(t['id']); usuario.value=str(t['usuario_id']); tecnico.value=str(t['tecnico_id']) if t['tecnico_id'] else ''; titulo.value=t['titulo']; descripcion.value=t['descripcion']; prioridad.value=t['prioridad']; estado.value=t['estado']; page.update()

    def eliminar(i):
        try:
            query('DELETE FROM tickets WHERE id=%s',(i,),False); aviso('Ticket eliminado'); cargar()
        except Exception as ex: aviso(str(ex),True)

    def asignar(i,tec):
        try:
            c=db(); cur=c.cursor(); cur.callproc('asignar_ticket',(i,tec)); c.commit(); c.close(); aviso('Ticket asignado mediante procedimiento'); cargar()
        except Exception as ex: aviso(str(ex),True)

    def cargar(e=None):
        try:
            q=f"%{buscar.value.strip()}%"
            datos=query('''SELECT t.*,u.nombre usuario_nombre,COALESCE(te.nombre,'Sin asignar') tecnico_nombre
            FROM tickets t JOIN usuarios u ON u.id=t.usuario_id LEFT JOIN tecnicos te ON te.id=t.tecnico_id
            WHERE t.titulo LIKE %s OR u.nombre LIKE %s OR t.estado LIKE %s ORDER BY t.id DESC''',(q,q,q))
            lista.controls=[]
            for t in datos:
                acciones=[ft.IconButton(ft.Icons.EDIT,on_click=lambda e,x=t:editar(x)),ft.IconButton(ft.Icons.DELETE,on_click=lambda e,x=t['id']:eliminar(x))]
                if not t['tecnico_id']:
                    acciones.append(ft.PopupMenuButton(items=[ft.PopupMenuItem(text=o.text,on_click=lambda e,x=t['id'],y=int(o.key):asignar(x,y)) for o in tecnico.options if o.key]))
                lista.controls.append(ft.Card(ft.Container(ft.Column([ft.Row([ft.Text(f"#{t['id']} · {t['titulo']}",size=18,weight=ft.FontWeight.BOLD),ft.Row(acciones)],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),ft.Text(f"{t['usuario_nombre']} · {t['tecnico_nombre']} · {t['prioridad']} · {t['estado']}"),ft.Text(t['descripcion'])]),padding=15)))
            r=query('SELECT estado,COUNT(*) total FROM tickets GROUP BY estado')
            resumen.controls=[ft.Chip(label=ft.Text(f"{x['estado']}: {x['total']}")) for x in r]
            page.update()
        except Exception as ex: aviso('Error de base de datos: '+str(ex),True)

    combos()
    page.add(ft.Text('MesaSimple TI',size=30,weight=ft.FontWeight.BOLD),ft.Text('Gestión simple de solicitudes de soporte'),resumen,ft.Divider(),ft.Text('Registrar / editar',size=20),ft.Row([usuario,tecnico]),ft.Row([titulo,prioridad,estado]),descripcion,ft.Row([ft.FilledButton('Guardar',icon=ft.Icons.SAVE,on_click=guardar),ft.OutlinedButton('Limpiar',on_click=limpiar)]),ft.Divider(),buscar,lista)
    cargar()

if hasattr(ft, 'app'):
    ft.app(target=main)
else:
    ft.run(main, view=ft.AppView.FLET_APP)

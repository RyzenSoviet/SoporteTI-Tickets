CREATE TRIGGER trg_ticket_creado
AFTER INSERT ON tickets
FOR EACH ROW
INSERT INTO historial_tickets (
    ticket_id,
    estado_anterior,
    estado_nuevo
)
VALUES (
    NEW.id,
    NULL,
    NEW.estado
);

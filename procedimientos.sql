CREATE PROCEDURE cambiar_estado_ticket(
    IN p_ticket INT,
    IN p_estado VARCHAR(30)
)
BEGIN
    DECLARE v_estado_anterior VARCHAR(30);

    SELECT estado INTO v_estado_anterior FROM tickets WHERE id = p_ticket;

    UPDATE tickets SET estado = p_estado WHERE id = p_ticket;

    INSERT INTO historial_tickets(
        ticket_id,
        estado_anterior,
        estado_nuevo
    )
    VALUES(
        p_ticket,
        v_estado_anterior,
        p_estado
    );
END;


CREATE PROCEDURE asignar_ticket(IN p_ticket INT, IN p_tecnico INT)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM tickets WHERE id = p_ticket) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ticket inexistente';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM tecnicos WHERE id = p_tecnico AND activo = 1) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Técnico inexistente o inactivo';
    END IF;

    UPDATE tickets SET tecnico_id = p_tecnico, estado = 'En proceso' WHERE id = p_ticket;
END;

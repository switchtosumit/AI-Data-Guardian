from db.database import get_connection


def save_incident(
    incident_type,
    severity,
    alert,
    root_cause,
    recommended_fix
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO incidents
        (
            incident_type,
            severity,
            alert,
            root_cause,
            recommended_fix
        )
        VALUES (%s,%s,%s,%s,%s)
        """,
        (
            incident_type,
            severity,
            alert,
            root_cause,
            recommended_fix
        )
    )

    conn.commit()
    cur.close()
    conn.close()
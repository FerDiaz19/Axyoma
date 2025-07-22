# Generated manually for admin_plantas table
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS admin_plantas (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                planta_id INTEGER NOT NULL REFERENCES plantas(planta_id) ON DELETE CASCADE,
                fecha_asignacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                status BOOLEAN DEFAULT TRUE,
                password_temporal VARCHAR(128),
                UNIQUE(usuario_id, planta_id)
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS admin_plantas;"
        ),
    ]


echo "- Eliminando migraciones actuales..."

if exist "apps\users\migrations" (
    for %%f in (apps\users\migrations\*.py) do (
        if not "%%~nxf"=="__init__.py" (
            del "%%f" 2>nul
            echo "-- Eliminado: %%~nxf"
        )
    )
)

if exist "apps\subscriptions\migrations" (
    for %%f in (apps\subscriptions\migrations\*.py) do (
        if not "%%~nxf"=="__init__.py" (
            del "%%f" 2>nul
            echo "-- Eliminado: %%~nxf"
        )
    )
)

if exist "apps\evaluaciones\migrations" (
    for %%f in (apps\evaluaciones\migrations\*.py) do (
        if not "%%~nxf"=="__init__.py" (
            del "%%f" 2>nul
            echo "-- Eliminado: %%~nxf"
        )
    )
)

if exist "apps\admin_bd\migrations" (
    for %%f in (apps\admin_bd\migrations\*.py) do (
        if not "%%~nxf"=="__init__.py" (
            del "%%f" 2>nul
            echo "-- Eliminado: %%~nxf"
        )
    )
)

echo "- Creando nuevas migraciones..."
python manage.py makemigrations
python manage.py migrate

echo "Migraciones listas. :)"

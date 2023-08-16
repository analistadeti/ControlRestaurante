import pyodbc
from django.shortcuts import render, redirect
from .models import PersonaSeleccionada
from django.db import transaction
from datetime import datetime

from datetime import date

def mostrar_personas(request):
    if 'habitacion' in request.GET:
        numero_habitacion = request.GET['habitacion']
        server = '192.168.32.102'
        database = 'zeusprueba'
        username = 'roxanne'
        password = 'Cr@2_no680*1996'

        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

        sql_query = f"""
           SELECT ACOMPANA.NROHAB_HAB as HABITACION,
                   IDENT_ACO AS CEDULA,
                   ACOMPANA.NOMBRE_ACO AS NOMBRE,
                   ACOMPANA.CODIGP_PLA,
                   DESCRI_PLA AS NOM_PLAN,
                   CARGOS.DESCRI_CAR AS ALIMENTACION,
                   FLLEGA_ACO AS LLEGADA,
                   FSALID_ACO AS SALIDA,
                   EDAD_ACO AS EDAD,
                   CONVERT(VARCHAR, GETDATE() , 23) AS FECHA_ACTUAL
            FROM ACOMPANA 
            INNER JOIN PLANES ON PLANES.CODIGP_PLA = ACOMPANA.CODIGP_PLA 
            INNER JOIN Acompa31 ON Acompa31.Nombre_aco = ACOMPANA.NOMBRE_ACO
            INNER JOIN PAQUETE ON PLANES.CODIGP_PLA = PAQUETE.CODIGP_PLA
            INNER JOIN CARGOS ON CARGOS.CCARGO_CAR = PAQUETE.CCARGO_CAR
            WHERE ACOMPANA.CODIGP_PLA NOT LIKE 'SO%' 
            AND ACOMPANA.ESTADO_ACO = '31' 
            AND CARGOS.DESCRI_CAR IN ('DESAYUNO', 'ALMUERZO', 'CENA', 'BEBIDA')
            AND ACOMPANA.NROHAB_HAB = '{numero_habitacion}'
            ORDER BY  CARGOS.DESCRI_CAR DESC;
        """
        cursor = conn.cursor()
        cursor.execute(sql_query)
        personas = cursor.fetchall()

        personas_seleccionadas = PersonaSeleccionada.objects.all()

        personas_a_mostrar = []

        for persona in personas:
            tiene_coincidencia = False
            fecha_objeto=datetime.strptime(persona.FECHA_ACTUAL,"%Y-%m-%d").date()
            for persona_sel in personas_seleccionadas:
                if (persona_sel.cedula == persona.CEDULA and
                        persona_sel.alimentacion == persona.ALIMENTACION and
                        persona_sel.fecha_actual == fecha_objeto ):
                    tiene_coincidencia = True
                    break


            if not tiene_coincidencia:
                personas_a_mostrar.append(persona)
        fecha_actual = datetime.today()
        personas_seleccionadas = PersonaSeleccionada.objects.filter(fecha_actual=fecha_actual)
        contador=len(personas_seleccionadas)


        return render(request, 'mostrar_personas.html',
                      {'personas': personas_a_mostrar, 'numero_habitacion': numero_habitacion,'contador':contador})
    return render(request, 'mostrar_personas.html')





def guardar_persona_seleccionada(request):
    if request.method == 'POST':
        habitacion = request.POST['habitacion']
        seleccionadas = request.POST.getlist('seleccionadas')  # Lista de cédulas seleccionadas
        server = '192.168.32.102'
        database = 'zeusprueba'
        username = 'roxanne'
        password = 'Cr@2_no680*1996'

        with transaction.atomic():  # Usar transacción para asegurar la integridad de la base de datos
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

            for seleccionada in seleccionadas:
                cedula, alimentacion = seleccionada.split('_')
                print(seleccionadas)
                sql_query = f"""
                    SELECT ACOMPANA.NROHAB_HAB as HABITACION,
                           IDENT_ACO AS CEDULA,
                           ACOMPANA.NOMBRE_ACO AS NOMBRE,
                           ACOMPANA.CODIGP_PLA,
                           DESCRI_PLA AS NOM_PLAN,
                           CARGOS.DESCRI_CAR AS ALIMENTACION,
                           FLLEGA_ACO AS LLEGADA,
                           FSALID_ACO AS SALIDA,
                           EDAD_ACO AS EDAD,
                           CAST(GETDATE() AS DATE) AS FECHA_ACTUAL
                    FROM ACOMPANA 
                    INNER JOIN PLANES ON PLANES.CODIGP_PLA = ACOMPANA.CODIGP_PLA 
                    INNER JOIN Acompa31 ON Acompa31.Nombre_aco = ACOMPANA.NOMBRE_ACO
                    INNER JOIN PAQUETE ON PLANES.CODIGP_PLA = PAQUETE.CODIGP_PLA
                    INNER JOIN CARGOS ON CARGOS.CCARGO_CAR = PAQUETE.CCARGO_CAR
                    WHERE ACOMPANA.CODIGP_PLA NOT LIKE 'SO%' 
                    AND ACOMPANA.ESTADO_ACO = '31' 
                    AND CARGOS.DESCRI_CAR IN ('DESAYUNO', 'ALMUERZO', 'CENA', 'BEBIDA') 
                    AND IDENT_ACO = '{cedula}'
                    AND CARGOS.DESCRI_CAR = '{alimentacion}'
                    AND ACOMPANA.NROHAB_HAB = '{habitacion}'
                    ORDER BY  CARGOS.DESCRI_CAR DESC;
                """

                cursor = conn.cursor()
                cursor.execute(sql_query)
                persona = cursor.fetchone()

                if persona:
                    persona_seleccionada = PersonaSeleccionada(
                        habitacion=habitacion,
                        cedula=persona.CEDULA,
                        nombre=persona.NOMBRE,
                        alimentacion=persona.ALIMENTACION,
                        nom_plan=persona.NOM_PLAN,
                        fecha_actual=persona.FECHA_ACTUAL
                    )

                    persona_seleccionada.save()

        return redirect('mostrar_personas')  # Redirige al listado de personas

    return render(request, 'mostrar_personas.html')

from django.shortcuts import render
from .models import PersonaSeleccionada
from datetime import datetime

def mostrar_personas_seleccionadas(request):
    fecha_actual = datetime.now().date()

    if request.method == 'GET' and 'fecha' in request.GET:
        fecha = request.GET['fecha']
        try:
            fecha_actual = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            pass

    personas_seleccionadas = PersonaSeleccionada.objects.filter(fecha_actual=fecha_actual)
    contador=len(PersonaSeleccionada.objects.filter(fecha_actual=fecha_actual))
    context = {
        'personas_seleccionadas': personas_seleccionadas,
        'fecha_actual': fecha_actual,
        'contador':contador
    }

    return render(request, 'mostrar_personas_seleccionadas.html', context)


# Review-Classifier

## Authors

- Daniel Ángel Arró Moreno
- Pedro Pablo Álvarez Portelles
- Abel Llerena Domingo


## Problema

El contenido de las reseñas generado por un usuario es útil para que los compradores tomen decisiones
más informadas en sitios web de compras en lı́nea. Sin embargo, debido al gran volumen de reseñas,
especialmente de artı́culos populares, es muy difı́cil para cualquiera encontrar fácilmente información
relevante. A menudo, el sitio web sólo proporciona algunos métodos de clasificación simples, pero no
muy útiles, como clasificación por tiempo o calificación por votos de utilidad. Se pueden considerar va-
rios factores para este propósito, incluido el historial de compras reciente del usuario y el de navegación
y las propiedades de los artı́culos.

Se propone un sistema que haga uso de lo antes mencionado, junto a otras caracterı́sticas que se consideran
necesarias, para que los compradores sugieran mejores compras a los usuarios.


## Requirements

- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- alembic
- pytest
- pytest-cov
- faker
- networkx
- numpy
- sklearn

## APIs

Se ha implementado un servicio API para probar el proyecto utilizando FastAPI y SQLalchemy para conexión a abse de datos. Dicha API contiene el endpoint __"/reviews/{user_id}/{product_id}"__ para poder devolver las reseñas filtradas utilizando el algoritmo propuesto.

## Implementation

Se ha utilizado un enfoque de arquitectura limpia para la elaboracion del proyecto. Se implementaron tests para poder probar que el filtro se ejecute correctamente y un apartado en la carpeta **metrics tests** para poder probar todas las métricas y evaluar la efectividad del SRI.

La aplicación simula estar integrada en un sistema _e-comerce_ lo cual se logra agregando las tablas que se esperan que estén presentes en dicho sistema para poder interactuar con las mismas y retornar la respuesta esperada.

### Description of Modules

- **alembic**: Archivos de configuraciones de las migraciones de la base de datos postgres utilizando alembic. **[NO MODIFICAR]**

- **app**: Contiene el código principal de la implementacion de la API del proyecto.

- **docs**: Contiene los archivos para compilar el reporte en latex.

- **metrics tests**: Contiene los archivos necesarios para poder medir el buen nivel del funcionamiento correcto de nuestro SRI aplicando diferentes métricas.

- **tests**: Contiene los tests con los que se muestran la efectividad de la API agregando diferentes datos para rellenar la base de datos y probar el funcionamiento del algoritmo.

- **app/application**: Contiene la declaración de los servicios que sirven como soporte para la implementación del algoritmo de filtrado de reseñas.

- **app/domain**: Contiene la declaración de los modelos de las tablas a utilizar en la API.

- **app/infrastructure**: Contiene la definicion de los repositorios encargados de interactuar con la base de datos y modificar y obtener los datos de las distintas tablas.

- **app/presentation**: Contiene la definción del `endpoint` de la API por la cual se va a acceder al servicio desde una fuente externa o desde el frontend.

## Script command description

### Build the image

- **create_venv**: Crea un entorno virtual llamado `venv` en el directorio actual e instala las dependencias listadas en `requirements.txt`. Si `virtualenv` no está instalado, lo instalará automáticamente.
  
  Comando para ejecutar:
  ```bash
  ./script.sh create_venv
  ```

- **activate_venv**: Activa el entorno virtual `venv`. Este comando debe ejecutarse antes de ejecutar otros comandos locales como `local_migrate` o `local_test`.

  Comando para ejecutar:
  ```bash
  ./script.sh activate_venv
  ```

- **build**: Construye los contenedores Docker.

  Comando para ejecutar:
  ```bash
  ./script.sh build
  ```

- **up**: Levanta los contenedores Docker en segundo plano.

  Comando para ejecutar:
  ```bash
  ./script.sh up
  ```

- **down**: Apaga los contenedores Docker.

  Comando para ejecutar:
  ```bash
  ./script.sh down
  ```

### Run migrations

- **migrate**: Ejecuta las migraciones de la base de datos en el entorno Docker.

  Comando para ejecutar:
  ```bash
  ./script.sh migrate
  ```

- **create_migration**: Crea una nueva migración de la base de datos con el mensaje proporcionado.

  Comando para ejecutar:
  ```bash
  ./script.sh create_migration "Mensaje de la migración"
  ```

- **local_migrate**: Ejecuta las migraciones de la base de datos localmente, utilizando el entorno virtual.

  Comando para ejecutar:
  ```bash
  ./script.sh local_migrate
  ```

### Run tests

- **test**: Ejecuta las pruebas unitarias dentro del contenedor Docker.

  Comando para ejecutar:
  ```bash
  ./script.sh test
  ```

- **local_test**: Ejecuta las pruebas unitarias localmente, utilizando el entorno virtual.

  Comando para ejecutar:
  ```bash
  ./script.sh local_test
  ```

### Run project

- **run_local**: Activa el entorno virtual y ejecuta la aplicación localmente. 

  Comando para ejecutar:
  ```bash
  ./script.sh run_local
  ```

- **open_swagger**: Abre la interfaz de Swagger en el navegador predeterminado en la URL `http://127.0.0.1:5000/swagger/`. Si `xdg-open` (para Linux) o `open` (para macOS) están disponibles, se utilizarán para abrir la URL automáticamente. De lo contrario, se imprimirá la URL para que la abras manualmente.

  Comando para ejecutar:
  ```bash
  ./script.sh open_swagger
  ```

## Steps to install and run the project locally

> [!NOTE]
> Puede ejecutar la parte principal del proyecto desde el archivo ubicado en **metrics tests/main1.ipynb**

1. **Crear y activar el entorno virtual**:
   ```bash
   ./script.sh create_venv
   ```

2. **Activar el entorno virtual:**
    ```bash
   source venv/bin/activate
   ```

3. **Instalar las dependencias::**
    ```bash
   ./script.sh install_deps
   ```

4. **Ejecutar la aplicación localmente**:
   ```bash
   ./script.sh run_local
   ```

5. **Abrir Swagger en el navegador**:
   Acceder a la ruta http://127.0.0.1:8000/docs

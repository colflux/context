# DevOps y CI/CD

Conceptos para que cualquier persona del equipo entienda cómo se automatiza el paso de "código escrito" a "código corriendo en producción", sin depender de pasos manuales. Surge del trabajo de despliegue automático del ecosistema COLFLUX (ver tarea `automatizar-deploy-ecosistema-colflux.md` en `personal/tasks/`).

## ¿Qué es DevOps?

Es la práctica de unir el trabajo de desarrollo (Dev) y operaciones (Ops) para que el código se entregue de forma rápida, frecuente y confiable. La idea clave: automatizar todo lo repetible (compilar, probar, desplegar) para que un push no dependa de que alguien se conecte al servidor a mano.

## Palabras clave

| Término | Qué significa |
|---|---|
| **CI** (Integración Continua) | Cada vez que alguien hace push, se compila/prueba el código automáticamente para detectar errores rápido |
| **CD** (Entrega/Despliegue Continuo) | Una vez pasa CI, el código se publica automáticamente (o con un clic) al servidor |
| **Pipeline** | La secuencia de pasos automatizados (build → test → deploy) |
| **Workflow** | En GitHub Actions, el archivo YAML que define un pipeline completo |
| **Job** | Un grupo de pasos dentro de un workflow (ej. "build", "deploy") — puede haber varios jobs, en paralelo o encadenados |
| **Step** | Una acción concreta dentro de un job (ej. "instalar dependencias", "conectarse por SSH") |
| **Runner** | La máquina (virtual, de GitHub o propia) donde se ejecutan los steps |
| **Trigger** | El evento que dispara el workflow (ej. `on: push` a la rama `main`) |
| **Secret** | Credencial sensible (llave SSH, password) guardada de forma cifrada en GitHub, nunca en el código |
| **Reusable workflow** | Un workflow que otros repos pueden invocar (`workflow_call`) en vez de duplicar el YAML |

## ¿Cómo funciona GitHub Actions?

Vive en la carpeta `.github/workflows/` de cada repo, como archivos `.yml`. Cuando ocurre el *trigger* (ej. push a `main`), GitHub levanta un *runner*, ejecuta los *jobs*/*steps* definidos, y si algún step falla, el workflow se marca en rojo — así el equipo se entera sin tener que revisar el servidor a mano.

En COLFLUX, el step final del job de deploy sería conectarse por SSH al servidor y correr `git pull && docker compose up -d --build`.

📖 [GitHub Actions — Understanding GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions)

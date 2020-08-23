## Sacchai Nepal Backend
`DRF` powered `REST API` backend using `django` and `django-rest framework`.

## Setup Instructions
- Clone the project inside suitable directory
```sh
git clone git@github.com:SachhaiNepal/Backend.git
```
- Create virtual environment for the project
```sh
cd <project-directory>
make virtual-env
```
- Activate just created `virtual environment`

    - For `windows` user
        ```sh
        source venv\Scripts\activate.bat
        ```
    - For `linux` user
        ```sh
        source venv/bin/activate
        ```
- Install requirements
```sh
make install
```
- Create database `migrations` and `tables`
```sh
make build
```
- Serve
```sh
make serve
```


# CyberCrim – IA-Solution

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern cybersecurity portfolio and interactive demo application featuring an OWASP vulnerability scanner. Built with Python, Flask, and Tailwind CSS.

## Features

- 🛡️ Interactive OWASP vulnerability scanner demo
- 📊 Real-time scan progress and results
- 📄 Generate PDF and JSON reports
- 🌓 Dark/light mode support
- 📱 Fully responsive design
- 🚀 Ready for deployment on Railway

## Prerequisites

- Python 3.8+
- Node.js 16+ (for Tailwind CSS)
- pip (Python package manager)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/cybercrim-ia-solution.git
   cd cybercrim-ia-solution
   ```

2. Create and activate a virtual environment:

   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install Node.js dependencies and build Tailwind CSS:

   ```bash
   # Installer les dépendances Node.js
   npm install
   
   # Construire les fichiers CSS (mode développement avec surveillance)
   npm run build:css
   
   # Ou pour une construction de production
   NODE_ENV=production npm run build:css
   ```

## Configuration PWA

L'application est configurée comme une Progressive Web App (PWA) avec les fonctionnalités suivantes :

- 🚀 **Installation** : Peut être installée sur l'écran d'accueil des appareils mobiles et des ordinateurs de bureau
- 📱 **Hors ligne** : Fonctionne hors ligne grâce au service worker
- 🔄 **Mises à jour** : Vérification automatique des mises à jour toutes les heures
- 🎨 **Thème** : Support du mode sombre/clair avec persistance

### Fichiers PWA

- `static/manifest.webmanifest` : Configuration de l'application (nom, icônes, couleurs)
- `static/service-worker.js` : Gestion du cache et des fonctionnalités hors ligne
- `static/img/icon-192.png` : Icône 192x192px pour les appareils Android
- `static/img/icon-512.png` : Icône 512x512px pour les écrans haute résolution

### Personnalisation

Pour personnaliser l'application PWA :

1. Mettez à jour `static/manifest.webmanifest` avec les informations de votre application
2. Remplacez les icônes dans `static/img/`
3. Ajustez les couleurs dans `tailwind.config.js`
4. Personnalisez le comportement du service worker dans `static/service-worker.js`

## Développement

### Structure des fichiers

- `static/src/input.css` : Fichier d'entrée CSS avec les directives Tailwind
- `static/css/styles.css` : Fichier de sortie généré par Tailwind
- `templates/` : Modèles Jinja2 pour les vues Flask
- `app.py` : Application Flask principale

### Commandes utiles

```bash
# Démarrer le serveur de développement Flask
flask run

# Construire les fichiers CSS en mode développement (avec surveillance)
npm run watch:css

# Construire les fichiers CSS pour la production
NODE_ENV=production npm run build:css

# Vérifier la configuration Tailwind
npx tailwindcss --help
```

### Configuration Tailwind

Le fichier `tailwind.config.js` est configuré avec :

- Mode sombre basé sur les classes (`.dark`)
- Couleurs personnalisées (`dark`, `primary`, `secondary`, `accent`)
- Polices personnalisées (Inter, Space Grotesk, Fira Code)
- Animations personnalisées (pulse-slow, float)
- Plugins : `@tailwindcss/typography` et `@tailwindcss/forms`

## Déploiement

Pour déployer l'application :

1. Construisez les fichiers CSS pour la production :
   ```bash
   NODE_ENV=production npm run build:css
   ```

2. Assurez-vous que le service worker est correctement enregistré et que les chemins des ressources sont valides

3. Déployez l'application sur votre hébergeur préféré (Railway, Heroku, Vercel, etc.)

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.

   ```bash
   # Installer les dépendances Node.js
   npm install
   
   # Construire les fichiers CSS (mode développement avec surveillance)
   npm run build:css
   
   # Ou pour une construction de production
   NODE_ENV=production npm run build:css
   ```

5. Create a `.env` file based on the example:

   ```bash
   cp .env.example .env
   ```

   Then edit the `.env` file with your configuration.

## Running Locally

1. Start the Flask development server:

   ```bash
   flask run
   ```

2. Open your browser and navigate to:

   ```text
   http://127.0.0.1:5000
   ```

## Building for Production

1. Install Gunicorn:

   ```bash
   pip install gunicorn
   ```

2. Build Tailwind CSS for production:

   ```bash
   NODE_ENV=production npm run build:css
   ```

3. Run with Gunicorn:

   ```bash
   gunicorn app:app
   ```

## Deployment

This application is ready to be deployed on Railway. Click the button below to deploy:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2Fyourusername%2Fcybercrim-ia-solution)

## Project Structure

```bash
cybercrim-ia-solution/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── tailwind.config.js     # Tailwind CSS configuration
├── static/                # Static files (CSS, JS, images)
│   └── css/
│       └── styles.css     # Compiled Tailwind CSS
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── tools.html         # Security tools showcase
│   ├── demo.html          # OWASP scanner demo
│   ├── certs.html         # Certifications
│   ├── services.html      # Services offered
│   └── contact.html       # Contact form
└── scanner/               # OWASP scanner module
    ├── __init__.py
    ├── engine.py          # Scanner logic
    └── report_generator.py # Report generation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OWASP](https://owasp.org/) for their security guidelines and resources
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Tailwind CSS](https://tailwindcss.com/) for the utility-first CSS framework

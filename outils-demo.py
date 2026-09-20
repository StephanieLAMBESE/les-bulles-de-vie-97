#!/usr/bin/env python3
"""Génère une version autonome du site en un seul fichier HTML.

Le CSS externe et toutes les images sont inlinés, afin que le fichier
puisse être envoyé par mail et ouvert sans serveur ni dossier assets.
"""
import base64, mimetypes, re, sys

SOURCE = 'index.html'
CIBLE = 'les-bulles-de-vie-97-demo.html'

BANDEAU = '''
  <div id="bandeau-demo" style="position:fixed;top:0;left:0;right:0;z-index:9999;background:#2C2C3E;color:#fff;
              font-family:sans-serif;font-size:13px;text-align:center;
              padding:8px 16px;line-height:1.4;">
    Version de démonstration — les liens externes (formulaire, e-mail, téléphone) sont actifs.
  </div>
  <script>
    (function () {
      function decaler() {
        var bandeau = document.getElementById('bandeau-demo');
        var nav = document.querySelector('nav');
        if (!bandeau || !nav) return;
        var h = bandeau.offsetHeight;
        nav.style.top = h + 'px';
        document.body.style.paddingTop = h + 'px';
      }
      // la nav n'est pas encore analysée à ce stade du document
      document.addEventListener('DOMContentLoaded', decaler);
      window.addEventListener('resize', decaler);
    })();
  </script>
'''


def data_uri(chemin):
    mime = mimetypes.guess_type(chemin)[0] or 'application/octet-stream'
    with open(chemin, 'rb') as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode('ascii')}"


def inliner_images(texte, prefixe_css=''):
    """Remplace les chemins assets/… par des data URI."""
    for chemin in sorted(set(re.findall(r"assets/[\w.-]+\.(?:webp|png|jpg|jpeg)", texte))):
        uri = data_uri(chemin)
        texte = texte.replace(f'"{chemin}"', f'"{uri}"').replace(f"'{chemin}'", f"'{uri}'")
    # base.css référence les images sans le préfixe assets/
    if prefixe_css:
        for chemin in sorted(set(re.findall(r"url\('([\w.-]+\.(?:webp|png))'\)", texte))):
            texte = texte.replace(f"url('{chemin}')", f"url('{data_uri(prefixe_css + chemin)}')")
    return texte


def main():
    html = open(SOURCE, encoding='utf-8').read()

    # 1. remplacer chaque feuille de style externe par son contenu
    for href in re.findall(r'<link rel="stylesheet" href="([^"]+)">', html):
        css = inliner_images(open(href, encoding='utf-8').read(), prefixe_css='assets/')
        html = html.replace(f'<link rel="stylesheet" href="{href}">',
                            f'<style>\n{css}\n</style>')

    # 2. inliner les images référencées depuis le HTML
    html = inliner_images(html)

    # 3. la page légale n'accompagne pas le fichier isolé : on évite le lien mort
    html = html.replace(
        '<a href="mentions-legales.html">Mentions légales</a> ·\n'
        '      <a href="mentions-legales.html#confidentialite">Confidentialité</a>',
        'Mentions légales · Confidentialité')

    # 4. marquer la page comme démonstration
    html = html.replace('<body>', '<body>\n' + BANDEAU, 1)
    html = re.sub(r'<title>.*?</title>',
                  '<title>Les Bulles de Vie 97 — Démo (nouvelle version)</title>',
                  html, count=1, flags=re.S)

    open(CIBLE, 'w', encoding='utf-8').write(html)

    restants = re.findall(r'(?:src|href)="(?!data:|https?:|#|mailto:|tel:)[^"]+"', html)
    print(f"{CIBLE} — {len(html.encode('utf-8')) // 1024} Ko")
    print("références externes restantes :", restants or "aucune")
    return 1 if restants else 0


if __name__ == '__main__':
    sys.exit(main())

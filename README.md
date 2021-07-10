# Discord-Embed-Markup
A markdown-like language for describing discord embeds

*Docs and implementation coming soon!*

The data in test.dem should translate to:
```json
{
    "title": "Try out Discord Embed Markup",
    "description": "You can describe embeds\nyay",
    "url": "https://github.com/xImAnton/Discord-Embed-Markup",
    "color": 16744192,
    "timestamp": "2009-02-14T00:31:30",
    "footer": {
      "icon_url": "https://cdn.discordapp.com/avatars/489766550451257345/b77b7a60da28e604ada933eb2773b2b4.png?size=1024",
      "text": "Made by"
    },
    "thumbnail": {
      "url": "https://discord.com/assets/f9bb9c4af2b9c32a2c5ee0014661546d.png"
    },
    "author": {
      "name": "Anton Vogelsang",
      "url": "https://ximanton.de"
    },
    "fields": [
      {
        "name": "This is a field",
        "value": "this is the text of the field",
        "inline": true
      },
      {
        "name": "second field",
        "value": "when the text of a field ends with &, it's an inline field",
        "inline": true
      }
    ]
  }
```

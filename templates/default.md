---
title: "{{topic}}"
date: "{{datetime}}"
author: "meeting-bot"
---

# {{topic}}

**Data:** {{datetime}}
**Duração:** {{duration}}

## 📋 Tópicos Tratados

{% for topic in topics %}
- {{topic}}
{% endfor %}

## ✔️ Decisões Importantes

{% for decision in decisions %}
- {{decision}}
{% endfor %}

## 🎯 Ações Definidas

{% for action in actions %}
- **{{action.owner}}** - {{action.task}} (até {{action.deadline}})
{% endfor %}

---
*Gerado automaticamente pelo meeting-bot*

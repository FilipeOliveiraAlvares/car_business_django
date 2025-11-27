# Configuracao Final do Railway

## Configuracao Recomendada

### Pre-deploy Command:
```
python manage.py migrate && python manage.py collectstatic --noinput
```

### Custom Start Command:
```
gunicorn core.wsgi
```

---

## O que cada comando faz

### Pre-deploy Command (executa antes de cada deploy):
- `python manage.py migrate` - Aplica migracoes do banco de dados
- `python manage.py collectstatic --noinput` - Coleta arquivos estaticos (CSS, JS, imagens)

### Custom Start Command (executa quando o container inicia):
- `gunicorn core.wsgi` - Inicia o servidor web

---

## Importar dados manualmente (quando necessario)

Se precisar importar novos modelos/versoes/marcas:

1. Acesse o terminal do Railway
2. Execute:
   ```bash
   python manage.py importar_dados
   ```

**Nota:** O comando nao importa categorias por padrao (ja foram importadas).

---

## Por que nao incluir importar_dados no Pre-deploy?

- Dados ja foram importados manualmente
- Evita erros de UNIQUE constraint a cada deploy
- Deploy mais rapido
- Importacao manual apenas quando necessario

---

## Checklist de Configuracao

- [ ] Pre-deploy Command configurado
- [ ] Custom Start Command configurado
- [ ] Variaveis de ambiente configuradas (SECRET_KEY, DEBUG, ALLOWED_HOSTS, etc.)
- [ ] DATABASE_URL configurada (criada automaticamente pelo PostgreSQL)
- [ ] CSRF_TRUSTED_ORIGINS configurado (se necessario)

---

**Configuracao otimizada e pronta para producao!**


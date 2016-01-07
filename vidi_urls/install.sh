#!/bin/bash

# Need to modify the base template:
# vi /opt/cantemo/portal/portal_themes/core/templates/base.html
# {% if vidi_urls %}
#     <div style="padding: 5px; background-color: black; position: fixed; bottom: 0px; z-index: 100;">
#     {% for url in vidi_urls %}
#         <a style="color: white;" href="{{ url }}" target="_blank">{{ url }}</a><br />
#     {% endfor %}
#     </div>
# {% endif %}


# Currently this does not work
match='<body class="{% block bodyclass %}base{% endblock %}" id="body">'
insert='{% if vidi_urls %}<div style="padding: 5px; background-color: black; position: fixed; bottom: 0px; z-index: 100;">{% for url in vidi_urls %}<a style="color: white;" href="{{ url }}" target="_blank">{{ url }}</a><br />{% endfor %}</div>{% endif %}'
file='/opt/cantemo/portal/portal_themes/core/templates/base.html'

sed -i 's/${match}/\n${insert}/' $file

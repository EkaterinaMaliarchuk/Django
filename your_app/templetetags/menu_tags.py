from django import template
from your_app.models import Menu, MenuItem

register = template.Library()

@register.inclusion_tag('menu_template.html', takes_context=True)
def draw_menu(context, menu_name):
    try:
        menu = Menu.objects.get(name=menu_name)
        menu_items = menu.items.filter(parent__isnull=True).prefetch_related('children')
        return {'menu_items': menu_items, 'current_path': context['request'].path}
    except Menu.DoesNotExist:
        return {'menu_items': []}

# menu_template.html
<ul>
    {% for item in menu_items %}
        <li>
            <a href="{{ item.url or item.named_url }}">{{ item.name }}</a>
            {% if item.children.exists %}
                <ul>
                    {% for child in item.children.all %}
                        <li>
                            <a href="{{ child.url or child.named_url }}">{{ child.name }}</a>
                        </li>
                    {% endfor %}
                </ul>
            {% endif %}
        </li>
    {% endfor %}
</ul>

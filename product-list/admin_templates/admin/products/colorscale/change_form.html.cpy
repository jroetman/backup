{% extends "admin/base_site.html" %}
{% load i18n admin_urls static admin_modify %}

{% block extrahead %}{{ block.super }}
<script type="text/javascript" src="{% url 'admin:jsi18n' %}"></script>
{{ media }}
{% endblock %}

{% block extrastyle %}{{ block.super }}<link rel="stylesheet" type="text/css" href="{% static "admin/css/forms.css" %}">{% endblock %}

{% block coltype %}colM{% endblock %}

{% block bodyclass %}{{ block.super }} app-{{ opts.app_label }} model-{{ opts.model_name }} change-form{% endblock %}

{% if not is_popup %}
{% block breadcrumbs %}
<div class="breadcrumbs">
<a href="{% url 'admin:index' %}">{% trans 'Home' %}</a>
&rsaquo; <a href="{% url 'admin:app_list' app_label=opts.app_label %}">{{ opts.app_config.verbose_name }}</a>
&rsaquo; {% if has_view_permission %}<a href="{% url opts|admin_urlname:'changelist' %}">{{ opts.verbose_name_plural|capfirst }}</a>{% else %}{{ opts.verbose_name_plural|capfirst }}{% endif %}
&rsaquo; {% if add %}{% blocktrans with name=opts.verbose_name %}Add {{ name }}{% endblocktrans %}{% else %}{{ original|truncatewords:"18" }}{% endif %}
</div>
{% endblock %}
{% endif %}

{% block content %}<div id="content-main">
{% block object-tools %}
{% if change %}{% if not is_popup %}
  <ul class="object-tools">
    {% block object-tools-items %}
      {% change_form_object_tools %}
    {% endblock %}
  </ul>
{% endif %}{% endif %}
{% endblock %}
<form {% if has_file_field %}enctype="multipart/form-data" {% endif %}action="{{ form_url }}" method="post" id="{{ opts.model_name }}_form" novalidate>{% csrf_token %}{% block form_top %}{% endblock %}
<div>
{% if is_popup %}<input type="hidden" name="{{ is_popup_var }}" value="1">{% endif %}
{% if to_field %}<input type="hidden" name="{{ to_field_var }}" value="{{ to_field }}">{% endif %}
{% if save_on_top %}{% block submit_buttons_top %}{% submit_row %}{% endblock %}{% endif %}
{% if errors %}
    <p class="errornote">
    {% if errors|length == 1 %}{% trans "Please correct the error below." %}{% else %}{% trans "Please correct the errors below." %}{% endif %}
    </p>
    {{ adminform.form.non_field_errors }}
{% endif %}

{% block field_sets %}
{% for fieldset in adminform %}
  {% include "admin/includes/fieldset.html" %}
{% endfor %}
{% endblock %}

{% block after_field_sets %}{% endblock %}

{% block inline_field_sets %}
{% for inline_admin_formset in inline_admin_formsets %}
    {% include inline_admin_formset.opts.template %}
{% endfor %}
{% endblock %}

{% block after_related_objects %}{% endblock %}

{% block submit_buttons_bottom %}{% submit_row %}{% endblock %}

{% block admin_change_form_document_ready %}
    <script type="text/javascript"
            id="django-admin-form-add-constants"
            src="{% static 'admin/js/change_form.js' %}"
            {% if adminform and add %}
                data-model-name="{{ opts.model_name }}"
            {% endif %}>
    </script>
{% endblock %}

{# JavaScript for prepopulated fields #}
{% prepopulated_fields_js %}

</div>
</form></div>
{% endblock %}

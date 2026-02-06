{% macro generate_schema_name(custom_schema_name, node) -%}
    {# 
      If a model specifies +schema: silver (or gold),
      we want the final schema to be exactly "silver" (or "gold"),
      not "analytics_silver".
    #}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}

{% macro c_to_f(col) %}
({{ col }} * 9/5) + 32
{% endmacro %}
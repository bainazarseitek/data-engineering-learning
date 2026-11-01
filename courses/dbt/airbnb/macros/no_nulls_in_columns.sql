-- Macro = a reusable Jinja function that RETURNS TEXT (usually SQL).
-- Call it from any model/test with {{ no_nulls_in_columns(ref('some_model')) }}.

{% macro no_nulls_in_columns(model) %}           {# define the macro; `model` is the input (a relation from ref()) #}
    SELECT * FROM {{ model }} WHERE              {# start the query; {{ model }} prints the real table name #}
    {% for col in adapter.get_columns_in_relation(model) -%}   {# ask Snowflake for the table's columns, loop over them #}
        {{ col.column }} IS NULL OR              {# for each column print "<column> IS NULL OR" #}
    {% endfor %}                                 {# end of the loop #}
    FALSE                                        {# closes the last "OR" so the SQL is valid #}
{% endmacro %}                                   {# end of the macro #}

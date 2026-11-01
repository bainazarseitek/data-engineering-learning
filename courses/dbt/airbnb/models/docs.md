{# docs blocks: long descriptions written in Markdown, used from .yml with "{{ doc('name') }}" #}

{% docs __overview__ %}
# Airbnb Berlin — dbt project
Raw Airbnb data (`AIRBNB.RAW`) is cleaned into dimensions and facts in `AIRBNB.DEV`.

Flow: **sources → src (ephemeral) → dim / fct → mart**.
{% enddocs %}

{% docs dim_listing_cleansed__minimum_nights %}
Minimum number of nights required to rent this property.

Keep in mind that old listings might have `minimum_nights` set to 0 in the source tables.
Our cleansing algorithm updates this to `1`.
{% enddocs %}

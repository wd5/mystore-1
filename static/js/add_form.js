django.jQuery(document).ready(function(){
    django.jQuery("select#id_category :first").attr("selected", "selected");
    django.jQuery("div.field-category").append("<div id='attributes_label' style='font-size:12px;font-weight:bold;padding:10px 0;'>Атрибуты товара наследуемые от категории:</div><div id='attribute_fields'>Категория не выбрана.</div>");
    function getFields (cat_val) {
        django.jQuery.getJSON("/ajax/category/",{id:+category_value}, function(j) {
            var new_fields = '';
            for (var i = 0; i < j.length; i++) {
                new_fields += '<label for="' + j[i].pk + '"">' + j[i].fields['name'] + '</label>';
                new_fields += '<input type="hidden" id="' + j[i].pk + '" name="attrn[]" value="' + j[i].pk + '"/>';
                new_fields += '<input type="text" id="' + j[i].pk + '" name="attrv[]"/>';
                new_fields += '<br /><br />';
            }
            django.jQuery("div#attribute_fields").empty().html(new_fields);
        })        
    }
    django.jQuery("select#id_category").change(function(){
        category_value = django.jQuery(this).val();
        if (category_value > 0) {
            getFields(category_value);
        }
        else {
            django.jQuery("div#attribute_fields").empty().html("Категория не выбрана.");
        }
    })
})

(function($) {
    $(function() {
        var selectField = $('#id_groupId'),
            groupInitialField = $('label[for=id_groupInitial], #id_groupInitial');

        function toggleGroupId(value) {
            value === true ? groupInitialField.show() : groupInitialField.hide();
        }

        // show/hide on change
        selectField.change(function() {
            console.log($(this).val());
            if (this.checked) {
                toggleGroupId(true)
            } else {
                toggleGroupId(false)
            }
        });
    });
})(django.jQuery);
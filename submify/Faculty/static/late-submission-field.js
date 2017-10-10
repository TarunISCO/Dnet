(function($) {
    $(function() {
        var selectField = $('#id_lateSubmission'),
            lateSubmissionField = $('label[for=id_lateSubmissionPeriod], #id_lateSubmissionPeriod');

        function toggleLatesSubmission(value) {
            value === true ? lateSubmissionField.show() : lateSubmissionField.hide();
        }

        // show/hide on change
        selectField.change(function() {
            console.log($(this).val());
            if (this.checked) {
                toggleLatesSubmission(true)
            } else {
                toggleLatesSubmission(false)
            }
        });
    });
})(django.jQuery);
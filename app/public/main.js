$(function () {
    $("#sendSms").click(function () {

        $.post('/send', {
            to: $("#phone").val(),
            productType: $('input[name=productType]:checked').val(),
            firstName: $("#firstName").val(),
            firstMessage: $("#firstMessage").val(),
            positiveResponse: $("#positiveResponse").val(),
            negativeResponse: $("#negativeResponse").val()
        }).done(function (response) {
            alert(response.status);
        }).fail(function (response) {
            alert(response);
        });
    });

    $("button[data-edit]").click(function (e) {
        var $target = $(e.currentTarget);
        var id = $target.attr('data-edit');
        var $ele = $("#" + id);
        if ($target.hasClass('edit')) {
            $ele.prop('disabled', false);
            $ele.css({
                "border-color": "black",
                "border-width": "1px",
                "border-style": "solid"
            });
            $ele.focus();
            $target.removeClass('edit').addClass('update').html('Update');
        } else {
            $ele.prop('disabled', true);
            $ele.css({
                "border-width": "0px"
            });
            $target.removeClass('update').addClass('edit').html('Edit');
        }
    });
});
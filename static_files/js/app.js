$(document).ready(function (e) {
    $('.add_to_cart').on('click', function (e) {

        e.preventDefault()
        let product_id = $(this).attr('data-id')

        $.ajax({
            url: "http://127.0.0.1:8000/order/add-to-cart",
            type: "POST",
            data: {

                product_id: product_id,
                quantity: 1
            },
            success: function (data) {


                // LOGIC
                $(".cart_html").html(data)

            },
            error: function (data) {
                alert(error)
            }
        })

    })

    $(document).on('click', ".delete_from_cart", function () {
        let id = $(this).attr('data-id')

        $.ajax({
            url: "http://127.0.0.1:8000/order/delete-from-cart",
            type: "POST",
            data: {
                product_id: id
            },
            success: function (html) {
                $("#table_body").html(html)
            },
            error: function (html) {
                alert("xato")
            }
        })

    })
})

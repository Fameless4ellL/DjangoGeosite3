
    $('.save').click(function () {
        window.print();
    });

    $(function () {

        $('article').each(function () {

            const _this = $(this);

            _this.readingTime({
                readingTimeTarget: _this.find('.eta'),
                wordCountTarget: _this.find('.words'),
                success: function (data) {
                    console.log(data);
                },
                error: function (data) {
                    _this.find('.eta').remove();
                }
            });
        });
    });
    function openNav() {
        document.getElementById("mySidenav").style.width = "250px";
        document.getElementById("main").style.marginLeft = "250px";
    }

    function closeNav() {
        document.getElementById("mySidenav").style.width = "0";
        document.getElementById("main").style.marginLeft = "0";
    }

    $(function () {
        $('#go-top').goTop({
            // top offset
            scrollTop: 100,
            // scroll speed in milliseconds
            scrollSpeed: 1000,
            // fade in/out speed in milliseconds
            fadeInSpeed: 1000,
            fadeOutSpeed: 500
        })
    });
    $(document).ready(function () {
        $('[data-toggle="popover"]').popover({
            placement: 'left',
            template: '<div class="popover" id="main" role="tooltip"><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
            trigger: 'hover',
            html: true,
        });
    });

    function googleTranslateElementInit() {
        new google.translate.TranslateElement({
            pageLanguage: 'ru',
            layout: google.translate.TranslateElement.FloatPosition.TOP_LEFT,
            autoDisplay: false
        }, 'google_translate_element');
    }

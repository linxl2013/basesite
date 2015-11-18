function setNav(){
    var demosubmenu = $('#demo-submenu');
    if (demosubmenu.length){
        if ($(window).width() < 450){
            demosubmenu.find('a:last').hide();
        } else {
            demosubmenu.find('a:last').show();
        }
    }
    if ($(window).width() < 767){
        $('.navigation-toggle').each(function(){
            $(this).show();
            var target = $(this).attr('data-target');
            $(target).hide();
            setDemoNav();
        });
    } else {
        $('.navigation-toggle').each(function(){
            $(this).hide();
            var target = $(this).attr('data-target');
            $(target).show();
        });
    }
}
function setDemoNav(){
    $('.navigation-toggle').each(function(){
        var target = $(this).attr('data-target');
        if (target == '#navbar-demo'){
            if ($(target).is(':visible')){
                $(this).css('margin-bottom', 0);
            } else {
                $(this).css('margin-bottom', '2.3em');
            }
        }
    });
}
$(function(){
    setNav();
    $(window).bind('resize', function(){
        setNav();
    });
    $('.navigation-toggle').bind('click', function(){
        var target = $(this).attr('data-target');
        $(target).toggle();
        setDemoNav();
    });

    $('#menu').tree({
        onClick: function (node) {
            if(node.attributes != undefined && node.attributes.url != undefined){
                if($('#tt').tabs('exists', node.text)){
                    $('#tt').tabs('select', node.text);
                }else{
                    $('#tt').tabs('add', {
                        width: '100%',
                        height: '100%',
                        title: node.text,
                        href: node.attributes.url,
                        closable: true,
                    });
                }
            }
        }
    });

    // $('#tt').tabs({
    //     onLoad: function(panel){
    //         // $(panel).addClass('content-doc');
    //         $(panel).height('100%');
    //     }
    // });

    /*$(window).resize(function(){
        // alert('ss');
        $('#dg').datagrid('resize', {
            // width: function(){return $('.tabs-panels panel:visible').width();},
            width: '100%',
            height: function(){
                return $(window).height()-65;
            },
        });
    });*/

});

function addFrom(text, url){
    if($('#tt').tabs('exists', text)){
        $('#tt').tabs('select', text);
    }else{
        $('#tt').tabs('add', {
            width: '100%',
            height: '100%',
            title: text,
            href: url,
            closable: true,
        });
    }
}

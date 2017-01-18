$(document).ready(function () {
    status_service('spark', 1)
    status_service('spark', 2)
    status_service('spark', 3)
    status_service('spark', 4)
    status_service('hdfs', 1)
    status_service('hdfs', 2)
    status_service('hdfs', 3)
    status_service('hdfs', 4)
    status_service('neo4j', 1)
    status_service('neo4j', 2)
    status_service('neo4j', 3)
    status_service('rabbitmq', 1)
    status_service('rabbitmq', 2)
    status_service('zookeeper', 1)
    status_service('zookeeper', 2)
    status_service('zookeeper', 3)
});

function status_service(name_service, id) {
    $.ajax({
        url: "/status_" + name_service + "/" + id,
        type: "GET",
        success: function () {
            success('#' + name_service + '-' + id)
        },
        error: function () {
            error('#' + name_service + '-' + id)
        }
    });
}

function start_service(name_service, id) {
    $.ajax({
        url: "/start_" + name_service + "/" + id,
        type: "GET",
        success: function () {
            status_service(name_service, id)
            location.reload();
        },
        error: function () {
            status_service(name_service, id)
            location.reload();
        }
    });
}

function stop_service(name_service, id) {
    $.ajax({
        url: "/stop_" + name_service + "/" + id,
        type: "GET",
        success: function () {
            status_service(name_service, id)
            location.reload();
        },
        error: function () {
            status_service(name_service, id)
            location.reload();
        }
    });
}


function success(id_balise) {
    $(id_balise).removeClass("label-danger");
    $(id_balise).addClass("label-success");
}

function error(id_balise) {
    $(id_balise).removeClass("label-success");
    $(id_balise).addClass("label-danger");
}
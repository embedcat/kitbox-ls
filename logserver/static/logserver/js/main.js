function MqttCmdSelectOnChange(obj) {
    let value = obj.value;
    console.log(value);
    publish_filter = document.getElementById("div_id_publish_filter");
    logger_filter = document.getElementById("div_id_logger_filter");

    publish_filter.style.display = "none";
    logger_filter.style.display = "none";

    if (value == 1) {
        publish_filter.style.display = "block";
    }
    if (value == 3) {
        logger_filter.style.display = "block";
    }
}
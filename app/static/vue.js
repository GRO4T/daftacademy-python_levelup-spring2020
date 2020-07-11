Vue.component("hello", {
    template: "<label>Input Your Name:<h1></h1><input/></label>"
});

Vue.component("bar", {
    template: "<div id='bar'></div>"
});

new Vue({
    delimiters: ['[[', ']]'],
    el: "#vue",
    data: {
        text: "This is a Vue app.",
        html: "<p id='green'>You can use Vue to do<br/>all kinds of cool stuff!</p>",
        html1: "<p>Here we'll use Vue to make a an app<br/>that says Hello! to you.</p>"
    },
    methods: {
        sayHi: function() {
            var name = document.querySelector("#vue input"),
                button = document.querySelector("#vue button"),
                prompt = "What's your name?";
            var style = name.style;

            if (!name.value || name.value === prompt) {
                name.value = prompt;
                name.focus();
            } else {
                alert("Hello " + name.value + "!");
                name.value = null;
                button.blur();
            }
        }
    }
});
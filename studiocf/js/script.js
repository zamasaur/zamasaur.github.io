window.addEventListener("load", () => {

    fetch("./js/data.json")
        .then(response => {
            return response.json();
        })
        .then(jsondata => {
            const text = jsondata["Diritto del mercato finanziario e degli intermediari"][0].question;

            document.querySelector('textarea').value = text;

            var utterance = new SpeechSynthesisUtterance();
            utterance.text = text;
            utterance.lang = 'it-IT';

            //utterance.pitch = 0.001;
            utterance.rate = 0.75;
            //utterance.voice = voices[0];
            //utterance.volume = 2;
            window.speechSynthesis.speak(utterance);
        });

});

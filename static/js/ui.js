// percentage event listeners
for (let name of ["volume", "taper"]) {
  // we use function, as this corresponds to the element
  let slider = document.querySelector(`input[name=${name}]`)
  slider.onchange = function () {
    document.querySelector(`div.percentage[name=${name}]`).innerText = `${Math.round(this.value * 100)}%`;
  };

  // call the change so that we get the percentage to show up immediately
  slider.onchange();
}

// create a config ticket to send to the server from all ui inputs
function collate_config() {
  let config = {};

  // numeric input types, can easily be retrieved in a loop
  for (let name of ["volume", "taper", "time_per_syllable", "stop_pause", "comma_pause", "interword_pause"]) {
    config[name] = Number(document.querySelector(`input[name=${name}]`).value);
  }

  // textual input, much be taken manually as it's the only one
  config.sentence = document.querySelector(`textarea[name=sentence]`).value;

  return config;
}

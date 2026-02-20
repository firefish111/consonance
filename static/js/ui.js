for (let name of ["volume", "taper"]) {
  // we use function, as this corresponds to the element
  let slider = document.querySelector(`input[name=${name}]`)
  slider.onchange = function () {
    document.querySelector(`div.percentage[name=${name}]`).innerText = `${Math.round(this.value * 100)}%`;
  };

  slider.onchange();
}

function collate_config() {
  let config = {};

  for (let name of ["volume", "taper", "time_per_syllable", "stop_pause", "comma_pause", "interword_pause"]) {
    config[name] = Number(document.querySelector(`input[name=${name}]`).value);
  }

  config.sentence = document.querySelector(`textarea[name=sentence]`).value;

  return config;
}

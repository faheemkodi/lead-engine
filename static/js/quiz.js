document.addEventListener("DOMContentLoaded", () => {
  showQuestion();
  previousQuestion();
  nextQuestion();
});

const questionContainer = document.getElementById("question-container");
const questions = questionContainer.querySelectorAll(".question");
const length = questions.length;
let currentQuestion = 0;

const nextButton = document.getElementById("next");
const prevButton = document.getElementById("prev");

const showQuestion = () => {
  for (let i = 0; i < length; i++) {
    if (i !== currentQuestion) {
      questions[i].classList.add("d-none");
    }
  }
  questions[currentQuestion].classList.remove("d-none");
  if (currentQuestion === 0) {
    prevButton.disabled = true;
  } else {
    prevButton.disabled = false;
  }
  if (currentQuestion === length) {
    nextButton.disabled = true;
  } else {
    nextButton.disabled = false;
  }
};

const hideQuestion = (currentQuestion) => {
  questions[currentQuestion].classList.add("d-none");
};

const toggleSubmit = () => {
  const submit = document.getElementById("submit");
  if (submit.classList.contains("d-none") === true) {
    submit.classList.remove("d-none");
  } else {
    submit.classList.add("d-none");
  }
};

const checkIfAnswered = () => {
  let answerContainer = document.getElementById(`a-${currentQuestion + 1}`);
  if (answerContainer.classList.contains("choices")) {
    let options = answerContainer.querySelectorAll("input");
    for (let i = 0; i < options.length; i++) {
      if (options[i].checked === true) {
        return true;
      }
    }
    return false;
  } else {
    if (answerContainer.querySelector("input").value.trim() === "") {
      return false;
    }
    return true;
  }
};

const nextQuestion = () => {
  document.querySelector("#next").onclick = () => {
    if (!checkIfAnswered()) {
      alert("Answer required!");
    } else if (currentQuestion < length - 1) {
      currentQuestion++;
      showQuestion();
    } else {
      hideQuestion(currentQuestion);
      toggleSubmit();
      currentQuestion++;
      nextButton.disabled = true;
    }
  };
};

const previousQuestion = () => {
  document.querySelector("#prev").onclick = () => {
    if (currentQuestion === length) {
      toggleSubmit();
    }
    currentQuestion--;
    showQuestion();
  };
};

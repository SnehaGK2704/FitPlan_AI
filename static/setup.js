const steps = document.querySelectorAll(".form-step");
const progress = document.getElementById("progress-bar");

let currentStep = 0;

const nextBtn = document.getElementById("nextBtn");
const prevBtn = document.getElementById("prevBtn");

function updateSteps(){

steps.forEach((step,index)=>{
step.classList.toggle("active",index===currentStep);
});

const percent=((currentStep+1)/steps.length)*100;
progress.style.width=percent+"%";

prevBtn.style.display=currentStep===0?"none":"inline-block";

if(step === steps.length - 1){
nextBtn.textContent = "Finish";

}else{
nextBtn.textContent="Next";
}

}

nextBtn.addEventListener("click",()=>{

if(currentStep<steps.length-1){
currentStep++;
updateSteps();
}else{
document.getElementById("profileForm").submit();
}

});

prevBtn.addEventListener("click",()=>{

if(currentStep>0){
currentStep--;
updateSteps();
}

});

updateSteps();
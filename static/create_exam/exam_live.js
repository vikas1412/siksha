let getExamTime;
getExamTime = () => {
    let duration = document.getElementById('duration').value;
    let details = duration.split(":");

    let durationHour = Number(details[0]);
    let durationMinute = Number(details[1]);
    let durationSecond = Number(details[2]);
// window.alert(durationHour + " : " + durationMinute + " : " + durationSecond);

    let end = new Date();
    console.log(end.getHours(), end.getMinutes(), end.getSeconds());
    end.setHours(end.getHours() + durationHour);
    end.setMinutes(end.getMinutes() + durationMinute);
    end.setSeconds(end.getSeconds() + durationSecond);
    console.log(end.getHours(), end.getMinutes(), end.getSeconds());

    let deadline = end.getTime();

    const time_remaining = setInterval(function () {
        let begin = new Date();
        let remainingTime = deadline - begin.getTime();
        let hour = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minute = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
        let second = Math.floor((remainingTime % (1000 * 60)) / 1000);

        let h = end.getHours() - begin.getHours();
        let m = end.getMinutes() - begin.getMinutes();
        let s = end.getSeconds() - begin.getSeconds();

        document.getElementById("time-remaining").innerText = hour + ":" + minute + ":" + second;

        if (remainingTime <= 0) {
            clearInterval(time_remaining);
            document.getElementById("time-remaining").innerHTML = "Time Expired!";
            window.location.replace('http://localhost:9000/exam/');
        }
    }, 1000);
    const durationDate = new Date("duration");
};

window.onload=getExamTime();

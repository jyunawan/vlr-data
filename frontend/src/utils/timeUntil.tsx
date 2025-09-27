export function timeUntil(date: Date) {
  var currentTime: Date = new Date();

  var seconds: number = Math.round(
    (date.getTime() - currentTime.getTime()) / 1000,
  );


  var days: number = Math.floor(seconds / (60 * 60 * 24));
  seconds %= 60 * 60 * 24;
  var hours: number =  Math.floor(seconds / (60 * 60));
  seconds %= 60 * 60;
  var minutes: number =  Math.floor(seconds / 60);

  days = days >= 0 ? days : 0;
  hours = hours >= 0 ? hours : 0;
  minutes = minutes >= 0 ? minutes : 0;

  return { days, hours, minutes };
}

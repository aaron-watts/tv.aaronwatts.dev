# tvschedule

Uses Github Workflow to generate a json file using the tv maze api.

Add shows to shows.py.

Use the json in a Google Apps Script to add entries to a Google Calendar.

Use the following script with a time triggered execution for automated updates of your shows to a calendar.

```js
const calendarId = 'your-tv-shows-calendar-id';

function getSchedule() {
  const repsonse = UrlFetchApp.fetch('your-raw-github-json-file');
  const data = JSON.parse(repsonse.getContentText());
  return data.schedule;
};

function addToCalendar(episode, calendar) {
  if(!!episode.airtime && !!episode.runtime) {
    const airstamp = new Date(episode.airstamp);

    calendar.createEvent(
      episode._links.show.name,
      airstamp,
      new Date(airstamp.getTime() + episode.runtime * 60000),
      {
        description: episode.description,
      }
    );
  } else {
    const airdate = new Date(episode.airdate);
    const enddate = new Date(airdate);
    enddate.setDate(enddate.getDate() + 1);

    calendar.createAllDayEvent(
      episode._links.show.name,
      airdate,
      enddate,
      {
        description: episode.description,
      }
    );
  }
};

function main() {
  const calendar = CalendarApp.getCalendarById(calendarId);
  const schedule = getSchedule();
  let startDate = new Date();
  let endDate = new Date();
  const eventList = [];

  for(let showID in schedule) {
    const episode = schedule[showID];

    const summary = !!episode.summary ? episode.summary : '';
    episode.description = `<b>S${episode.season}E${episode.number} ${episode.name}</b>\n${summary}\n${showID}:${episode.id}`;

    const airstamp = new Date(episode.airstamp);
    if (airstamp.getTime() < startDate.getTime()) startDate = airstamp;
    if (airstamp.getTime() > endDate.getTime()) endDate = airstamp;
  };

  const events = calendar.getEvents(startDate, endDate);
  
  for (let event of events) {
    const description = event.getDescription();
    const descriptionSplit = description.split(/\W+/);
    const showId = descriptionSplit[descriptionSplit.length - 2];
    const episodeId = descriptionSplit[descriptionSplit.length - 1];
    eventList.push(showId);

    if (schedule[showId]
      && episodeId == schedule[showId].id
      && schedule[showId].description != description
    ) event.setDescription(schedule[showId].description);
  };

  for (let showID in schedule) {
    const episode = schedule[showID];
    if (eventList.indexOf(showID) < 0) {
      addToCalendar(episode, calendar);
    }
  }
};
```
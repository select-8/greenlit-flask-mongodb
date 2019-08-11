# DATA CENTRIC DEVELOPMENT MILESTONE PROJECT

## GREENLIT

## Project Overview

The project presented [here](https://select-8.github.io/charting-ms2/#) consists of a series of interactive graphs and charts. They are rendered in SVG by D3.js, charted using the DC.js charting library and made multidimentially interactive by the crossfilter.js JavaScript library. 

The goals of this project are to:



### User Stories

Three types of users:
 - Non registered browser
 - Registered user
 - Admin


##### As a user... 


### Data Model

### UX
#### Wireframe

#### Typography


### Features


##### Login/Register


##### View


##### Filter / Sort


##### Add


##### Edit


##### Vote


##### Remove / Delete


##### Content / Messaging

If not yet added a pitch
If select Matt Damon
If not add title and / or genre
On remove / Delete

##### Admin

Charts

Users as row chart so it can expnad over time. Not really scaleable right now.
Time chart would be nice.


#### Left to Implement

Talent Profiles
Pagination
Block submit until Edit
Charts
Better User data
    - user own stats page / profile
UX
    - messaging
Multiple Query Parameters 


## Testing

Manual

	- if no pitches exist in collection what happens?
		- for non logged in
		- for logged in
			- in own ps
			- in all ps
		- for admin	
	- If not pitches in collection, all_ps displays no genre of that type message
	- if user does not use sentence case on text input, what happens?
		- in edit
		- in view
    - if user maually enters url endpoints

##### Users


##### Responsiveness


##### Browsers
The site was tested in Chrome, FireFox, Safari and Opera.

##### Chart Interactions


   

### Validation

HTML AND CSS files where found to be valid via the offical W3 code validators.

HTML : https://validator.w3.org/

CSS : https://jigsaw.w3.org/css-validator/

JavaScript files were tested at : https://jshint.com/

## Deployment

The site is deployed to GitHub Pages under the following process:


## Technologies Used

##### LANGUAGES
- [HTML](https://www.w3.org/html/)
- [CSS](https://www.w3.org/Style/CSS/Overview.en.html)
- [JavaScript](https://www.javascript.com/)
- SQL

##### VERSION CONTROL
- [GIT](https://git-scm.com/)

##### FRAMEWORKS
- [Bootstrap](https://getbootstrap.com/)

To create a responsive grid
- [jQuery](https://jquery.com/)

To create the dropdown information effect
- [D3](https://d3js.org/)

To render the charts in the DOM as SVG
- [dc.js](https://dc-js.github.io/dc.js/)

Provided templates for the charts
- [crossfilter.js](https://square.github.io/crossfilter/)

Provides multidimentional filtering of data in dc charts
- [queue.js](https://github.com/d3/d3-queue)

Evaluates asynchronous tasks to handle callbacks
##### APIs
 - [Google Fonts](https://fonts.google.com/)

##### SOFTWARE AND SERVICES
- [Visual Studio Code](https://code.visualstudio.com/)
- [GitHub](https://github.com/)

##### RDBMS
- [PostgreSQL](https://www.postgresql.org/)

##### EDITORS
- SUBLIME
- ATOM

##### VMWARE
- UBUNTU V18.04

##### HARDWARE
- MAC OSX

##### PROJECT MGMT
- SLACK
- NOTION

## Credits

A significant amount of the JavaScript in graph.js was based on the Code Institute D3 modules.

The code to remove NULL rows from the results of a crossfilter was found [here](https://github.com/dc-js/dc.js/wiki/FAQ#remove-empty-bins)


The DC example sets found [here](https://dc-js.github.io/dc.js/examples/) provided some of the methods for dealing with valueAccessors and working with chart labels and colours.
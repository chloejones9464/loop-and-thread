## Table Of Contents:
1. [Design & Planning](#design-&-planning)
    * [User Stories](#user-stories)
    * [Wireframes](#wireframes)
    * [Typography](#typography)
    * [Colour Scheme](#colour-scheme)

    
2. [Features](#features)
    * [Navigation](#Navigation)
    * [Footer](#Footer)
    * [Home page](#Home-page)
    * [Other features](#Other-features)

3. [Technologies Used](#technologies-used)
4. [Testing](#testing)
5. [Bugs](#bugs)
6. [Deployment](#deployment)
7. [Credits](#credits)

## Design & Planning:

### User Stories
Write your user stories in this section
### Wireframes
Attach wireframes in this section
### Typography
Explain font you've used for your project
### Colour Scheme
Screenshoot of the colour scheme for your project

## Features:
Explain your features on the website,(navigation, pages, links, forms.....)
### Navigation
### Footer
### Other features
## Technologies Used
List of technologies used for your project...
HTML
CSS
Bootstrap
Github
Django
Python
## Testing
Important part of your README!!!
### Google's Lighthouse Performance
Screenshots of certain pages and scores (mobile and desktop)
### Browser Compatibility
Check compatability with different browsers
### Responsiveness
Screenshots of the responsivness, pick few devices (from 320px top 1200px)
### Code Validation
Validate your code HTML, CSS (all pages/files need to be validated!!!), display screenshots
### Manual Testing user stories or/and features
Test all your user stories, you an create table 
User Story |  Test | Pass
--- | --- | :---:
paste here you user story | what is visible to the user and what action they should perform | &check;
- and attach screenshot

## Bugs

**TemplateDoesNotExist: `base.html`**  
  - *Cause*: The `base.html` file was not placed in the correct templates directory or not properly referenced.  
  - *Fix*: Created a `templates` folder at the project level, added `DIRS` in `settings.py`, and confirmed the correct template path.  

**Reverse URL error (`NoReverseMatch`)**  
  - *Cause*: Used `{% url 'pattern_list' %}` without having the correct `app_name` or namespace defined in `urls.py`.  
  - *Fix*: Added `app_name = 'patterns'` in the app’s `urls.py` and updated all `{% url %}` references.  

**Navbar logo not displaying**  
  - *Cause*: Incorrect path to static files.  
  - *Fix*: Confirmed logo placement inside `static/images/` and updated the template with `{% static 'images/logo.png' %}`.  

**Favicon not appearing in browser tab**  
  - *Cause*: Multiple favicon sizes weren’t properly referenced.  
  - *Fix*: Added all favicon sizes to `static/images/` and referenced them correctly in `base.html`.  

**Account migrations error (`table "account_emailaddress" already exists`)**  
  - *Cause*: Duplicate migrations from re-running `makemigrations` on the Allauth `account` app.  
  - *Fix*: Reset migration files and re-applied clean migrations.  

**CountryField error (`BlankChoiceIterator` object has no attribute `__len__`)**  
  - *Cause*: Incorrect field configuration for `CountryField`.  
  - *Fix*: Updated model to use `CountryField(blank_label="Country *", null=False, blank=False)`.  

**Hero image not centered**  
  - *Cause*: Background image CSS not set correctly.  
  - *Fix*: Used `background-position: center; background-size: cover;` in CSS.  

**Search bar border radius issue**  
  - *Cause*: Border radius only applied to one element (input vs. button).  
  - *Fix*: Grouped input + button inside a flex container and applied consistent border radius.  

**Pattern card images displaying different sizes**  
  - *Cause*: Uploaded images had inconsistent aspect ratios.  
  - *Fix*: Applied CSS with `aspect-ratio` and `object-fit: cover` for uniform card sizing.  

**Stripe Card Element not mounting**  
- *Cause*: Script used jQuery (`$`) to access keys, but jQuery was not included, causing a `ReferenceError`.  
- *Fix*: Added jQuery via CDN in `base.html`, ensuring `$` is defined and the Stripe Card Element mounts correctly.  

## Deployment

#### Creating Repository on GitHub
- First make sure you are signed into [Github](https://github.com/) and go to the code institutes template, which can be found [here](https://github.com/Code-Institute-Org/gitpod-full-template).
- Then click on **use this template** and select **Create a new repository** from the drop-down. Enter the name for the repository and click **Create repository from template**.
- Once the repository was created, I clicked the green **gitpod** button to create a workspace in gitpod so that I could write the code for the site.
#### Deloying on Github
The site was deployed to Github Pages using the following method:
- Go to the Github repository.
- Navigate to the 'settings' tab.
- Using the 'select branch' dropdown menu, choose 'main'.
- Click 'save'.

## Credits
List of used resources for your website (text, images, snippets of code, projects....)
  - Code & Text Content
   - Crispy forms 
   - Django GitHub docs
   - Pixelied - PNG to WEBP Converter
   - Bootstrap docs
   - Google Fonts
   - FontAwesome
   - Favicon
   - ColorSpace
   - ChatGPT
   - Allauth

  - Media
  
  - Acknowledgment
    - acknowledgment to mentors, peers, tutors, friends, family, facilitator (who ever contributed and helped with the project)

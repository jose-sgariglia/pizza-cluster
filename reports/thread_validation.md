# Validazione Pattern Thread — JMAIL Dataset

> Campione 10,000 email · seed=42 · separato dal censimento originale

---

## 1. Overlap OUTLOOK_HEADER_BLOCK ∩ CHEVRON_QUOTE

- Email con `CHEVRON_QUOTE`: **405** (4.0%)
- Email con `OUTLOOK_HEADER_BLOCK`: **465** (4.7%)
- Email con **entrambi**: **20** (0.2% del campione, 5% delle email chevron)

### Classificazione automatica (Outlook header dentro '>' vs blocchi separati)

- Header Outlook **dentro** righe chevron (annidato): **0** (0%)
- Header Outlook in blocco **separato/sequenziale**: **20** (100%)

### Sotto-campione: 20 body raw con entrambi i pattern

> Nota: body troncati a 3000 chars se più lunghi; '↵' = newline effettivo.

#### Esempio 1 — [SEPARATO] subj: `RE: Jeffrey Epstein`
*sender: Feierstein, Kim y*

```
Perfect....sorry one little call took so much planning for!!!

Original Message
From: Lesley Groff [mailto:
Sent: Wednesday, August 17, 2011 1:48 PM
To: Feierstein, Kimberly
Subject: Re: Jeffrey Epstein

HI again! Jeffrey will call Glenn through the office at 4pm today. Thanks so much for your help..

On Aug 17, 2011, at 1:34 PM, Feierstein, Kimberly wrote:

> Glenn just said he can do 4:00 NY time. Let me know if that works.

>

> -----Original Message--- > From: Lesley Groff [mailto: > Sent: Wednesday, August 17, 2011 1:34 PM > To: Feierstein, Kimberly > Subject: Re: Jeffrey Epstein

>

> ok, I also just sent JE an email asking if 2pm would be ok...you would think he would want earlier...

>

> On Aug 17, 2011, at 1:32 PM, Feierstein, Kimberly wrote: > >> Oh, I read before 3:00...let me recheck with glenn.

>>

>> Original Message » From: Lesley Groff [mailto: » Sent: Wednesday, August 17, 2011 1:29 PM » To: Feierstein, Kimberly >> Subject: Re: Jeffrey Epstein >> » let me see if Jeffrey can do 2:00...he was requesting after 3pm our time for some reason..

>>

>>

>> On Aug 17, 2011, at 1:27 PM, Feierstein, Kimberly wrote: >> >>> Ok, how is 2:00 NY time? What number should we call? >>> >>> Original Message----- >>> From: Lesley Groff [mailto: >>> Sent: Wednesday, August 17, 2011 12:45 PM >>> To: Feierstein, Kimberly >>> Subject: Re: Jeffrey Epstein >>> >>> ok super...now just let me know the time once you get it >>> and we are good to go! :) >>> thanks >>> >>> On Aug 17, 2011, at 12:33 PM, Feierstein, Kimberly wrote: >>> >>>> Best is definitely that he calls the office and I will connect.

EFTA R1_00878089
EFTA02184654

>>>>

>>>> -----Original Message---

>>>> From: Lesley Groff [mailto:)]

>>>> Sent: Wednesday, August 17, 2011 12:04 PM >>>> To: Feierstein, Kimberly >>>> Subject: Re: Jeffrey Epstein

>>>>

>>» that would be great...and I just spoke to JE...he asked that I get a number for JE to call him on...possibly, he should just call you at the office and you would connect Jeffrey to Glenn? is that best?..you tell me and I will have Jeffrey do it..

>>»

>>»

>>» On Aug 17, 2011, at 12:01 PM, Feierstein, Kimberly wrote:

>>>>

>>>» Not oversees....ok so when he calls in I will get a time from him and let you know.

>>>>>

>>>>> -----Original Message---

>>>>> From: Lesley Groff [mailto: >>>>> Sent: Wednesday, August 17, 2011 11:58 AM >>>>> To: Feierstein, Kimberly >>>>> Subject: Re: Jeffrey Epstein

>>>>>

>»» maybe I misdialed? or maybe it is MY pho
… [TRONCATO — originale 7,123 chars]
```

#### Esempio 2 — [SEPARATO] subj: `Fwd: Life Hotel - Rosenthal Note`
*sender: Amengual, Randolph*

```
Begin forwarded message:

From: Stephen Hanson <
Date: March 12, 2018 at 5:09:06 PM EDT
To: Miriam Blemur < >, HOWIE / SUE MUCHNICK
> "Randolph. / David Life Laywer 17 / Amengual"
Subject: Re: Life Hotel - Rosenthal Note

Punch line is that 50k loan does not help- as I stated I am $30k overdrawn as of Thur with out additional funding

Not to mention another winter storm coming our way and the 15 day Forecast is for a cooler then normal March end

I can not go deeper into debt personally and with out the 100k loan to guide us through the next 6-8 weeks there is at least an $100k of possible exposure - not to mention the additional $225 k I have lent the hotel through my personal credit card for needed hotel items over the last year that is on the hotels books It is apparent david has made plans for this event as no one would ever jeopardize millions of dollars of value for what is a $50k spread between us

This now all seems to tie into the harassment and obstruction of information towards restaurant Mgmt and myself spearheaded by david

EFTA00860142

We will be notifying any future restaurant reservations starting tomorrow of the restaurant closing - I would assume you have made similar provisions with hotel staff

Sent from my iPad
```

#### Esempio 3 — [SEPARATO] subj: `FW: Greatest movie line ever`
*sender: Zelin, Barry*

```
Barry W Zelin

Axiom Capital Management

780 Third Avenue

New York, NY 10017

* **Sender:** Sidney Horowitz
* **Recipient:** Zelin, Barry
* **Date Sent:** Tuesday, July 10, 2012 1:14 PM
* **Subject:** FW: Greatest movie line ever

This is not a chart. The key information in the image is:

* **From:** (Sender's email address is redacted)
* **To:** (Recipient's email addresses are redacted)
* **Subject:** FW: Greatest movie line ever
* **Date:** Tue, 10 Jul 2012 10:39:29 -0400

From:

EFTA00637980

Date: Tue, 10 Jul 2012 09:46:08 -0400 Subject: Fwd: Fw: Fwd: Greatest movie line ever To:

From: 
To: 
Sent: 7/6/2012 3:10:13 . Eastern Daylight Time [ ]
Subj: Fwd: Fw: Fwd: Greatest movie line ever

From: 
To: 
Sent: 7/6/2012 3:07:36 Eastern Daylight Time [ ]
Subj: Fw: Fwd: Greatest movie line ever

Robert A. Heinimann, Jr.
Attorney at Law
708 Orange Street
Apt. # 3
New Haven, CT 06511

--- - On Fri, 7/6/12, Robert Heinimann wrote:

This is an email header. The key information is:
* **From:** Robert Heinimann
* **Subject:** Fw: Fwd: Greatest movie line ever
* **To:** rick flanders, Gilhooly, Bob Oven, Frank Shanigan, Joseph Ernano, Gerry wiz, Robert Heinimann, Tommy SR, Tommy Heinimann Jr, Joe Lanzetta, Claire Bennett, Laura McNierney, Julianne Heinimann, Dennis, Ed Mahoney, Rich Vernier, Chris Behan, Mairead Mensching, Michael Ross, JAMES WALL
* **Date:** Friday, July 6, 2012

Date: Friday, July 6, 2012, 3:05 PM

>> Enjoy this 24 second clip. This is THE greatest movie

» line... EVER !

>>

> > > Most people say the greatest movie line was Clark Gable's

EFTA00637981

>> delivery to Vivien Leigh in Gone With the Wind: "Frankly, my dear, I don't give » a damn." >>> > > > But in reality the greatest, most accurate, and most >> timely movie line came from Bob Hope. > > > It came from a film made in 1940 >> entitled "The Ghost Breaker", with Paulette Goddard, Richard Carlson, and Bob » Hope. >>> WMV video file ATTACHED!

This email message is for the individual use of the intended recipients and may contain confidential and privileged information. Any unauthorized review, use, disclosure or distribution is prohibited. If you are not the intended recipient, please contact the sender by reply email and destroy all copies of the original message. Any views expressed in this message are those of the individual sender, except where the sender specifically states them to be the views of Axiom Capital Management.

Axiom Capital Management Inc. reviews and archives outgoi
… [TRONCATO — originale 3,407 chars]
```

#### Esempio 4 — [SEPARATO] subj: `RE: Jeffrey Epstein`
*sender: Jeskewitz, Jeannine*

```
Lesley,

The meeting is from 10am - 2pm on Nov. 26th. I'll hold the night of the 25th. jj

-----Original Message-----
From: Lesley Groff [mailto:|
Sent: Wednesday, September 12, 2012 04:25 PM
To: Jeskewitz, Jeannine
Subject: Re: Jeffrey Epstein

No worries. Maybe we should do both nights for now... I think it really depends on the itinerary of the conference. Does it start early on 26th? Or is it an evening thing? If early, I would think Jeffrey would want to stay night of 25th to be there for the early 26th arrival to event. ... If event is late on 26th he may only want to stay the 26th. Do you have the details of the event?

Sent from my iPhone

On Sep 12, 2012, at 5:11 PM, "Jeskewitz, Jeannine" wrote:

> Lesley,
>
> Please confirm which night you wanted the rooms for? Nov 25 or 26?
>
> I have a little confusion from my end, sorry.
>
> Thank you,
> Jeannine
>
>
>
> -----Original Message--
> From: Lesley Groff [mailto:|
> Sent: Wednesday, September 12, 2012 03:00 PM
> To: Jeskewitz, Jeannine
> Subject: Re: Jeffrey Epstein
>
> super deal! thank you!
>
On Sep 12, 2012, at 3:53 PM, Jeskewitz, Jeannine wrote:
>
>> Yes. 1 suite and 1 king on hold.
>> jj
>>
>> -----Original Message----
>> From: Lesley Groff [mailto:|
>> Sent: Wednesday, September 12, 2012 02:23 PM
>> To: Jeskewitz, Jeannine
>> Subject: Re: Jeffrey Epstein
>>
>> ok, all sounds great! To double check, are you able to hold one suite and one regular
room for Jeffrey?

>>

EFTA00405164

>> >> On Sep 12, 2012, at 3:21 PM, Jeskewitz, Jeannine wrote: >> >>> I received your email and have held the rooms for JE. >>> >>> I'll get back to you on their meeting just as soon as TJP tells me his plans. Promise. :o) >>> >>> jj >>> >>> Original Message >>> From: Lesley Groff [mailto: >>> Sent: Wednesday, September 12, 2012 10:04 AM >>> To: Jeskewitz, Jeannine >>> Subject: Re: Jeffrey Epstein >>> >>> Good morning Jeannine...just checking back in...I didn't hear back from you regarding the 2 requested rooms...just want to make sure the email was reed... >>> >>> (and you are probably still awaiting an answer on breakfast...no worries...I am holding it in his itinerary!) >>> >>> >>> On Sep 10, 2012, at 3:38 PM, Jeskewitz, Jeannine wrote: >>> >>» Lesley, >>>> >>>> Let me check with TJP. I'll come back to you shortly. >>>> Great news on the consortium, let me know if he'll stay overnight and if I can help with a reservation at the Park Hyatt Chicago or Hyatt Regency Chicago. >>>> >>>> jj >>>> >>>> Original Message >>>
… [TRONCATO — originale 4,776 chars]
```

#### Esempio 5 — [SEPARATO] subj: `RE: Jeffrey Epstein Conf. Call`
*sender: Lisa B. Toney*

```
Hopeful that we both will know before 5:00 :)

Lisa B. Toney
LEGAL ASSISTANT TO
HENRY BURNETT AND CHRISTOPHER E. KNIGHT

---Original Message---
From: [mailto:
Sent: Friday, September 23, 2011 3:56 PM
To: Lisa B. Toney.
Subject: Re: Jeffrey Epstein Conf. Call

ok, thanks ...I will remain patient...(will I know before 5pm today you think?) :)

On Sep 23, 2011, at 3:54 PM, Lisa B. Toney wrote:

> Hi , still trying to determine what time, if possible, on Sunday evening. Thanks for
your patience!
>
>
>
>
• > Lisa B. Toney
> LEGAL ASSISTANT TO
> HENRY BURNETT AND CHRISTOPHER E. KNIGHT

EFTA00427010

ΑΛΛΛΛΛΛΛΛ

> Original Message-----
> From: [mailto:
> Sent: Friday, September 23, 2011 2:43 PM
> To: Lisa B. Toney
> Subject: Jeffrey Epstein Conf. Call

>

• > Hi Lisa...sorry to bother you, but I am being asked if a time preference for the conference call Jeffrey would like to have this Sunday with Chris and Joe has been discussed or decided upon?? Can you let me know where they stand with this?

>

thanks so much,

• > **TAX MATTERS- IRS Circular 230 Disclosure: To ensure compliance with requirements imposed by the IRS, we inform you that any tax advice contained in this communication (including attachments) was not intended or written to be used, and cannot be used, for the purpose of (i) avoiding penalties under the Internal Revenue Code or (ii) promoting, marketing or recommending to another party any transaction or matter addressed herein. If you would like such advice, please contact us.*** ***Attention: The information contained in this E-mail message is attorney privileged and confidential information intended only for the use of the individual(s) named above. If the reader of this message is not the intended recipient, you are hereby notified that any dissemination, distribution or copy of this communication is strictly prohibited. If you have received this communication in error, please contact the sender by reply E-mail and destroy all copies of the original message. Thank you.

**TAX MATTERS- IRS Circular 230 Disclosure: To ensure compliance with requirements imposed by the IRS, we inform you that any tax advice contained in this communication (including attachments) was not intended or written to be used, and cannot be used, for the purpose of (i) avoiding penalties under the Internal Revenue Code or (ii) promoting, marketing or recommending to another party any transaction or matter addressed herein. If you would like such advice, please contact us.**
… [TRONCATO — originale 3,017 chars]
```

#### Esempio 6 — [SEPARATO] subj: `Re: Dan Ariely`
*sender: Unknown*

```
will do

On Sep 20, 2011, at 12:43 PM, Jeffrey Epstein wrote:

get two tickets

On Tue, Sep 20, 2011 at 11:24 AM,

>

wrote:

The only info the web site gives for the Friday night event is below:

evening-from 6-9 pm on "Irrationality Friday, September is the 23, Real 2011. Invisible Hand"- curated by Dan Ariely. Promises to be an amazing

It says sold out, but clearly Dan can get you a ticket if you would like to attend. Please advise

Begin forwarded message:

From: Dan Ariely >

Date: September 20, 201110:22:04 AM EDT

To:

Subject: Re: Jeffrey Epstein

Friday:

http://www.eventbrite.com/event/196183289S

Saturday:

http://behavioraleconomics.eventbrite.com/

if Jeffrey wants a ticket, just let me know

1

EFTA R1_00088777
EFTA01775039

Irrationally yours

Dan

http://danariely.com/

On Sep 20, 2011, at 10:03 AM, ██████████ wrote:

Hello Dan...Hope you are well...wondering if you could pass along the details of your conference this Friday Sept. 23rd in NY...Jeffrey is asking...

- The image contains the text "Thanks so much," followed by a black rectangle, then "Assistant to Jeffrey Epstein", and finally a larger black rectangle.
- The surrounding text indicates a query about details for a conference on Friday, September 23rd in NY, being asked by Jeffrey.
- The image appears to be a portion of a signature or closing of a message from an assistant to Jeffrey Epstein.

*********

The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. It is the property of Jeffrey Epstein Unauthorized use, disclosure or copying of this communication or any part thereof is strictly prohibited and may be unlawful. If you have received this communication in error, please notify us immediately by return e-mail or by e-mail to jeevacation@gmail.com <mailto:jeevacation@gmail.com> , and destroy this communication and all copies thereof, including all attachments. copyright -all rights reserved

2

EFTA_R1_00088778
EFTA01775040

3

EFTA R1_00088779
EFTA01775041
```

#### Esempio 7 — [SEPARATO] subj: `Re:`
*sender: Unknown*

```
Today?? You have lunch with Steve Kosslyn at 12.

On Tue, May 3, 2011 at 8:15 AM, Jeffrey Epstein <jeevacation@gmail.com> wrote:

> yes,, come at 12? 9 east 71 st??

On Tue, May 3, 2011 at 8:13 AM, <Unknown> wrote:

> Morning so I survived the met in one piece with no awful stories other than it was emotional and I went home to bed (big gold star) how are you honey and when are you free or are you free? X

Sent using BlackBerry® from Orange

From: Jeffrey Epstein <jeevacation@gmail.com>
Date: Sun, 1 May 2011 21:42:03 -0400
To: <Unknown>
Subject: Re:

I didn't call anyone, I will find out

<Unknown> wrote:

> Sorry I didn't come and see you today, I didn't feel great and didn't leave my hotel. As you called my mother you know where I am, Calling my mother is out of bounds!!! I would not call yours! I will be free after tomorrow and I HOPE we can see each other then. Love

Sent using BlackBerry® from Orange
```

#### Esempio 8 — [SEPARATO] subj: `Re: Jeffrey Epstein`
*sender: Lesley Groff*

```
Ok thanks

Sent from my iPhone

On May 19, 2016, at 3:59 PM, █████ <███████████████> wrote:

It is

Sent from my Windows Phone

From: Lesley Groff
Sent: 2016-05-19 22:57
To: 
Subject: Re: Jeffrey Epstein

...for your friend...birthday- - so is it or ? need to make sure correct!

On May 19, 2016, at 2:33 PM, ██████ <██████████████████>
wrote:

I have traveled through Moscow from New york already, so i didn't need visa there..

Sent from my Windows Phone

From:  <u>Lesley Groff</u>
Sent: 2016-05-19 <u>21:28</u>
To:
Subject:  Re: Jeffrey Epstein
M, if you go through Moscow to get back to Vilnius do you need a transit visa? do you know?
<u>On May 19, 2016, at 1:56</u> PM,
> wrote:
Of course:

EFTA_R1_00592037
EFTA02052354

Sent from my Windows Phone

From: Lesley Groff
Sent: 2016-05-19 20:42
To: 
Subject: Re: Jeffrey Epstein

great...and can you get me your friends also?

- Passport Number: [REDACTED]
- Date of Expiry: [REDACTED]
- An email was written on May 19, 2016, at 1:35 PM.

Sent from my Windows Phone

From: <u>Lesley Groff</u>
Sent: <u>2016-05-19 20:11</u>
To:
Subject: Re: Jeffrey Epstein

, I am being asked for your passport numbers please..
On May 19, 2016, at 12:16 PM,  <  > wrote:

Passport expires 04-07-2021

Sent from my Windows Phone

From: <u>Lesley Groff</u>
Sent: <u>2016-05-19 19:00</u>
To:
Subject: Re: Jeffrey Epstein

yes…that should be just fine…I need to know when your friend’s
passport expires please…

On May 19, 2016,
at 2:12 AM,

EFTA_R1_00592038
EFTA02052355

wrote:

Hello, Lesley..

Would it be possible if we could come back to Vilnius 24th or 25th of June??

Sent from my Windows Phone

From: <u>Lesley Groff</u>
Sent: <u>2016-05-18 22:16</u>
To:
Subject: Re: Jeffrey Epstein

Ok, thanks for the information.. will get back to you!

On
May
18,
2016,
at 3:04
<u>PM,</u>

wrote:

Hello Lesley!

How are you? My friend's name-

nationa
lity-

EFTA_R1_00592039
EFTA02052356

We would like to return about after 2 weeks from Vilnius.

Thank you!

Sent from my Windows Phone

From: <u>Lesley Groff</u>
Sent: <u>2016-05-18 17:27</u>
To:
Subject: Jeffrey Epstein

Hello ..1 understand you and a friend want

to
come
to NY
on
June
15th?
Can
you
please
give
me the
full
name
as it
appear
s on
your
friends
passpo
rt?
What
is her
nationa
lity?

EFTA_R1_00592040
EFTA02052357

What is her birthdate?
When do you want to return?
Tell me the name of the airport you need to depart from...

Thanks,
Lesley
Assistant to Jeffrey Epstein

EFTA_R1_00592041

EFTA0205235
… [TRONCATO — originale 2,501 chars]
```

#### Esempio 9 — [SEPARATO] subj: `Re: Itinerary INCL TICKETNO for| 17JAN17`
*sender: [redacted]*

```
no direct flights on 15th or 16th departing 1am or thereabouts...

On Jan 3, 2017, at 1:30 PM, [redacted] wrote:

Unless there is aim or 2am on the 16th or late night on the 15th direct but if there isn't then let's do the 9:35am:)

On Tue, Jan 3, 2017 at 1:28 PM — > wrote:

or we can do the 9:35am arriving 12:pm same price…maybe this one is better…?

On Jan 3, 2017, at 1:20 PM, =| wrote: Great. Let's do it. Thank you so so so much! On Tue, Jan 3, 2017 at 1:20 PM | = wrote: yes, 1 AM on 16th so you arrive early on 16th in NY at JFK

On Jan 3, 2017, at 1:18 PM, wrote:

To confirm that is lam on the 16th so it would arrive in NYC at 6am on the 16th as well?

On Tue, Jan 3, 2017 at 1:17 PM =

>= wrote:

Let's do lam on the 16th:)

On Tue, Jan 3, 2017 at 1:16 PM

= wrote:

Let's do lam

On Tue, Jan 3, 2017 at 1:03 PM = wrote:

there is also Cathay #890 to Newark for the same price departing 6:20pm arriving Newark 9pm… the sooner you let me know the better…thanks

EFTA00461809

On Jan 3, 2017, at 12:49 PM, > wrote:

Hi

Any changes on any flights on the 15 or 16 to NYC or Boston?

Thanks:)
On Tue, Dec 27, 2016 at 8:03 PM [redacted] < [redacted] > wrote:
For sure

Sent from my iPhone
On = Dec 27, 2016, at 6:22 PM, [redacted] < [redacted] > wrote:

Okay cool. I = think watching that January 16th flight to Boston (or even the January = 15th flights to NYC) to see if they change is the best bet! If no = changes, not a problem, but we might as well keep monitoring for the = next few weeks :)

On Dec 27, 2016, at 4:05 = PM, [redacted] <> [redacted] > = wrote:

Today: Nothing= to Boston (and probably not will be available), but you can fly to = NYC on January 14th, add coil = $882.00. Will keep watching

Sent from my iPhone

On Dec 24, 2016, at 12:57 PM, > wrote:

14, 15, and 16 to NY or Boston would all be good = options to check for

On Sat, Dec 24, 2016 at 11:40 AM wrote:

yes! for sure!

On Dec 23, 2016, at 6:54 PM, > wrote:

Yes let's keep for the 17th and just keep monitoring = flights on the 15th and 16th to both NY and Boston if that's okay? Than yi2u!! On Fri, Dec 23, 2016 at 6:52 PM = =I='< > = wrote:

Hey nE2=8A6the Amex = rep just called me back=E2=80=A6incredibly, to change the ticket to = depart on the 16th now is $1700 more! This can happen! He said it = is possible the airline changes it back but you never know=E2=80=A6there = is limited availability and that has something to do with it=E2=80=A6Not = sure if you still want to change to the 16th? We cou
… [TRONCATO — originale 11,648 chars]
```

#### Esempio 10 — [SEPARATO] subj: `Re:`
*sender: Jeffrey Epstein*

```
I applaud your determination.

On Fri, Aug 13, 2010 at 2:28 PM, a wrote:

> That is why I don't like any synthetic pills and I am sorry I took it.

Sent via BlackBerry from T-Mobile

From: Jeffrey Epstein <u><jeevacation@gmail.com></u>
Date: Fri 13 Au 2010 <u>14:10:06</u> -0400
To:  <
Subject: Re:

- This is exactly what i mean , it is manurafctued like any other industrial chemical, without the necesssary testing.. you need to study, you need to read , you need to look, and see. not just believe. The melatonin in dietary supplements is generally manufactured <mark>synthetically</mark> but is chemically identical to the melatonin produced in the body. Supplements arc required to list their source of melatonin ifmade directly from <mark>plant or animal sources.</mark> If the source is not given, it is assumed to be synthetic. However, neither the U.S. Food and Drug Administration (FDA) or any other state or federal agency routinely tests supplements for quality prior to sale. Consequently, ConsumerLab.com conducted their own tests on melatonin supplements to determine if they met label claims, to make sure they disintegrated properly and ensure they did not contain unacceptable levels oflead, a potential contaminant.

On Fri, Aug 13, 2010 at 1:51 PM, <██████████████████████> wrote:

> Melatonin is naturally produced in our bodies

Sent via BlackBerry from T-Mobile

From: Jeffrey Epstein <u><jeevacation@gmail.com></u>
Date: Fri 13 Au 2010 <u>12:55:52</u> -0400
To:  <
Subject: Re:

melatonin is a supplement , not a drug„ IT is more dangerous , it has not undergone testing,

On Fri, Aug 13, 2010 at 12:46 PM, a wrote:

> For example I took two pills of melatonin last night for better sleep and I woke up 10am this morning so sleepy S000 lazy... Messed up all my day :)

EFTA_R1_00187474
EFTA01816173

Now on my way to Hamtons!!! Weee! First time this summer! Have a good day Jeffrey!

Sent via BlackBerry from T-Mobile

From: Jeffrey Epstein <u>ieevacation(agmail.com></u>
Date: <u>Fri 13 Au 2010 07:17:18</u> -0400
To:
Subject:

You use the Internet , cell phone. email, text, wear clothes that contain polyester, shoes that have rubber, shop in stores with electric lights, carry bags made of plastic., travel by air, and subway.. These things are crcatcdby science„ . eating an apple as many effects„ most unknown, taking an aspirin has been studied for years. I understand your reluctance, and as i can see I am patient. JUst look around you , most of the things you do ar
… [TRONCATO — originale 4,999 chars]
```

#### Esempio 11 — [SEPARATO] subj: `FW: Jeffrey Epstein`
*sender: Yeon Cramer*

```
Hi Rachel,

Can you please respond to Leslie’s question below?

Thanks,

Yeon

From: Lesley Groff [mailto: ]
Sent: Thursday, February 28, 2013 12:08 PM
To: Yeon Cramer
Subject: Re: Jeffrey Epstein

...Jeffrey wants to make sure that whatever time wheels up should be for Mr. Gates is what he will do....Jeffrey doesn't want Mr. Gates to have to sit around and wait...if his helicopter is due to take off at I lam, Jeffrey can go earlier...please let me know what time Mr. Gates heli is planned for tomorrow when you have a moment. Thanks so much..

On Feb 28, 2013, at 1:53 PM, Yeon Cramer wrote:

Would it be possible to have warm lunch prepared for him?

Thank you,

Yeon

From: Lesley Groff [mailto:
Sent: Thursday, February 28, 2013 10:52 AM

EFTA00394560

To: Yeon Cramer
Cc: 
Subject: Re: Jeffrey Epstein

there is always food on the plane! Would you like to request something specific for Mr. Gates.? I have CC'd here who takes care of the food for the airplane

[ ]

On Feb 28, 2013, at 1:41 PM, Yeon Cramer wrote:

One more thing...
Will there be catering on the flight?

From: Lesley Groff [mallto
Sent: Thursday, February 28, 2013 9:07 AM
To: Yeon Cramer
Subject: Re: Jeffrey Epstein

of course...if I can be of further assistance, just let me know!

On Feb 28, 2013, at 12:00 PM, Yeon Cramer wrote:

Correct. Thank you for checking.

From: Lesley Groff [mailto
Sent: Thursday, February 28, 2013 8:05 AM
To: Yeon Cramer
Subject: Re: Jeffrey Epstein

EFTA00394561

Hello Yeon...just want to confirm you are coordinating Mr. Gates ground transportation upon arrival in Palm Beach?

On Feb 27, 2013, at 6:25 PM, Yeon Cramer wrote:

Thank you!

From: [mailto:]
Sent: Wednesday, February 27, 2013 3:25 PM
To: ; Yeon Cramer
Cc: Rachel Strege
Subject: Re: Jeffrey Epstein

Hello,

Depart Teterboro NJ, F.B.O. Atlantic Aviation Friday noon

Arrival West Palm Beach, F.B.O. Galaxy Aviation

flight time 2+30min

arrival West Palm Beach 2:30pm

thank you,
Larry Visoski
cell

In a message dated 2/27/2013 6:20:29 P.M. Eastem Standard Time, writes:

Yes, I am just awaiting the FBO info from our pilot and arrival time in Palm Beach. As soon as he gets back to me I will pass along all info together

Sent from my iPhone

On Feb 27, 2013, at 6:16 PM, Yeon Cramer < > wrote:

> Hi Lesley,

EFTA00394562

> Can you please confirm the information below for the Friday flight with Jeffrey and Bill from New York to Palm Beach? >

> Aircraft tail number
> Contact number for flight crew
> Departure airpor
… [TRONCATO — originale 2,843 chars]
```

#### Esempio 12 — [SEPARATO] subj: `Re: Jeffrey Epstein`
*sender: Biegel, Chelsie*

```
Thanks!

-----Original Message-----
From: Lesley Groff
Sent: Tuesday, January 28, 2014 3:19 PM
To: Biegel, Chelsie
Subject: Re: Jeffrey Epstein

nothin...I asked him this morning...I will let him know you are following up.

On Jan 28, 2014, at 3:17 PM, Biegel, Chelsie wrote:

> Hi Lesley,
>
> Just following up about the Norway meeting any word from Jeffrey?
>
> Thanks!
> Chelsie
```

#### Esempio 13 — [SEPARATO] subj: `Re:`
*sender: Jeffrey Epstein*

```
give me a number to call

On Fri, Mar 9, 2012 at 9:12 AM, Farkas, Andrew L. < => wrote:

You'll have it before noon. Shall 1 scan it to this email address?

Original Message-----
From: jeffrey epstein <u>[mailto:jeevacation@gmail.com]</u>
Sent: Friday, March 09, 2012 05:33 AM
To: Farkas, Andrew L.
Subject: Re:

Term sheet ??

Sony for all the typos .Sent from my iPhone

On Mar 9, 2012, at 7:23 AM, "Farkas, Andrew L." < > wrote:

> I don't understand.
>
> Original Message
> From: jeffrey epstein <u>[mailto:jeevacation@gmail.com]</u>
> Sent: Friday, March 09, 2012 02:19 AM
> To: Farkas, Andrew L.
>
> My guy leaves Tomorw ????
>
> Sony for all the typos .Sent from my iPhone
>
```

#### Esempio 14 — [SEPARATO] subj: `Re: Re:`
*sender: Richard Joslin*

```
The forms for power of attorney have been circulated for signature. FYI

On Tue, Mar 11, 2014 at 9:54 AM, Jeffrey Epstein <jeevacation@gmail.com> wrote:

> Forwarded message
> From: Melanie Spinella <
> Date: Tue, Mar 11, 2014 at 9:43 AM
> Subject: RE: Re:
> To: Jeffrey Epstein <jeevacation@gmail.com>

> Then it has to be prepared in the Family office and sent here

From: Jeffrey Epstein [mailto:jeevacation@gmail.com]
Sent: Tuesday, March 11, 2014 9:42 AM
To: Melanie Spinella
Subject: Re:

we need another with different dates asap for years 2007 -2010

> On Tue, Mar 11, 2014 at 9:03 AM, Melanie Spinella
> wrote:

> You are an early bird! - Leon signed the latest one last week

-----Original Message-----
> From: jeffrey epstein [mailto:jeevacation@gmail.com]
> Sent: Tuesday, March 11, 2014 4:30 AM
> To: Melanie Spinella
> Subject:

> Please provide new poa for rich 07-10. Note time Ev

> Sent from my iPad

This email and any files transmitted with it are confidential and intended solely for the person or entity to whom they are addressed and may contain confidential and/or privileged material. Any review, retransmission, dissemination or other use of, or taking of any action in reliance upon this information by persons or entities other than the intended recipient is prohibited. If you have received this email in error please contact the sender and delete the material from any computer.

> Apollo Global Management, LLC

EFTA_R1_00386570
EFTA01933389

A

The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. It is the property of Jeffrey Epstein Unauthorized use, disclosure or copying of this communication or any part thereof is strictly prohibited and may be unlawful. If you have received this communication in error, please notify us immediately by return e-mail or by e-mail to jeevacation@gmail.com, and destroy this communication and all copies thereof, including all attachments. copyright -all rights reserved

This email and any files transmitted with it are confidential and intended solely for the person or entity to whom they are addressed and may contain confidential and/or privileged material. Any review, retransmission, dissemination or other use of, or taking of any action in reliance upon this information by persons or entities other than the intended recipient is prohibited. If you have received this email in error ple
… [TRONCATO — originale 3,254 chars]
```

#### Esempio 15 — [SEPARATO] subj: `Re: Fw: AG China`
*sender: Jeffrey Epstein*

```
Exactly what I thought , do it

On Thursday, June 20, 2013, wrote:

The image is not a chart. It is an email header.

Key information:
*   **Sender:** Richard Merkin
*   **Date:** Thursday, June 20, 2013, 10:11:14
*   **Subject:** RE: AG China

David,

At this time I'm only willing to commit $5M. I'll split the difference with you and do 17.5%. I'm extremely busy at this time as I'm working on a number of projects, some of which may be beneficial to the project we are discussing. If this works for you please confirm and we can schedule some time to go into more detail.

Thanks

----Original Message
From: [mailto:
Sent: Wednesday, June 19, 2013 1:30 PM
To: Richard Merkin
Subject: Re: AG China

20% for 7M? And importantly your advice, guidance and support for our growth? You have my full commitment to make this a success and to do good! Original Message----- From: Richard Merkin Date: Wed, 19 Jun 2013 10:44:48 To: 'David Stern'< Subject: RE: AG China

How about 5M for 20% ? Would that work for you?

Original Message-----
From: David Stern [mailto:
Sent: Tuesday, June 18, 2013 1:11 PM
To: Richard Merkin
Subject: Re: AG China

Dear Dick,

Were you able to consider my reply yesterday? Is this something that may work for you?

I would be delighted to come to LA to see you which would - as always - be a true joy, with the added bonus

EFTA00963307

of getting exposed to US sports and some California sun (while we have rain storms in Europe....) !

All the best

David

On 17 Jun 2013, at 17:29, Richard Merkin wrote:

> David,
>
> I remember last time you thought I may be requiring too much for the investment. I don't have at my fingertips what you thought was too much. I know you currently have 100% of the company, what do you suggest would be an appropriate equity stake that you think I would feel would be fair and appropriate for me to invest? If this is something agreeable, I would be happy to meet and discuss further. Maybe another Lakers game? Or even a Dodgers game.
>
> -----Original Message-----
>
> From: David Stern [mailto:
>
> Sent: Monday, June 17, 2013 9:18 AM
>
> To: Richard Merkin
>
> Subject: Re: AG China
>
> Apologies for the late reply, I just returned from China.
>
> Main progress is that the product is finalised ("Health Insurance Information Processing and Analytics System").
>
> It has been approved by the central government and we are on the way of becoming national standard for payment processing based on our data standardization engine.
>
>
… [TRONCATO — originale 4,411 chars]
```

#### Esempio 16 — [SEPARATO] subj: `Re: Apartments`
*sender: [Redacted]*

```
Yes, send the dirty ones to the same cleaners would be great...We need to check on the other linens and towels that are supposed to be there for the other apartments. Sue was under the impression they had been delivered as well....What is the name and phone number of the dry cleaners?

On Dec 19, 2012, at 10:49 AM, Rosalyn Fontanilla wrote:

I only got linens for 10B only shall I send the dirty towels and linens here cleaners

On Dec 19, 2012 10:13 AM, "| > wrote:

Begin forwarded message:

From: 
Subject: Re: Apartments
Date: December 19. 2012 9:43:47 AM EST
To:  Rosalyn Fontanilla <

Please check

10B: 95818
ION: 67451
11B: 7931
IIP: 20334

Sounds like I1P should be complete with fresh linens and towels already on the bed and in bathroom ready to go...but I do not know for sure. 10B, ION and 11B need the fresh linens and towels for sure. Thanks!

On Dec 19, 2012, at 9:14 AM, Rosalyn Fontanilla wrote:

What all apt do I have to go and give the codes pls.

On Dec 19, 2012 8:06 AM, ' a wrote: Super! So Lyn please go today and let me know when you have finished! Thanks Sent from my iPhone On Dec 19, 2012, at 7:55 AM, > wrote: > The laundry has arrived back, it is the linen for apartments 10 b , 10 n and 11 p >

EFTA00399237

> Sent from my iPhone

> On Dec 19, 2012, at 1:45 PM, > wrote:

>> Morning Lyn. Heads up... We are going to need you to check out all the apartments ...double check they have been cleaned properly, soap in dispensers etc and put clean linens on the beds and towels in the closets and in bathrooms. Sue was having the laundry done and delivered to the apartments. She thought it should be at 301 by today or tomorrow. Perhaps you can call the doorman and ask today if the cleaning has arrived Please let me know ! Thanks so much >>

>> Sent from my iPhone

EFTA00399238
```

#### Esempio 17 — [SEPARATO] subj: `Fwd: RE: RE: 31E-MM-108062 victim Report`
*sender: [redacted]*

```
██████ - fyi below. Thanks for forwarding ██████ email. We have this handled and wanted to keep you aware.

I'm heading to Germany now but if you need me I will have my phone.

<u>Thanks</u> and have a great weekend!

---------- Forwarded message ---------
From: "██████████████████████████████████████████>
Date: Jul 26, 2019 3:28 PM
Subject: RE: RE: 31E-MM-108062 victim Report
To: "████████████████████████████████████████████>,"Crutchfield, ████████(CID) (FBI)"
<ccrutchfield@fbi.gov>
Cc: "██████████████████████████████████████████>

Hi

Congrats on being able to gain experience through such a case!

Attached is the 'Contact Report' from VNS. VNS is the Victim Notification System which allows us to meet our legal obligation to notify and provide rights to victims of federal crimes. The system is tied to FBI, USAO, BOP, USPIS and the Marshalls. Victims only need one login and password to track the entire legal life of the case.

Thecontact report shows all the information that is currently recorded in VNS. The TOTAL VICTIM list is from SA Young and contains all victims that have been identified. The review is what I was working on, on the high side. The details I need are on the high side email I will send you shortly after this email.

Our goal on the victim services side is to make sure all victims are in VNS and that | has worked her magic with them. The 'math' is the Total Victim sheet (all victims) minus contact report victims (already in VNS) equals the review spreadsheet (still need to be added to VNS, and has missing data).

I am here today until 5:30 so please feel free to call if you want to talk through anything.

Thank you,

EFTA01649243

From: ██████████████████████)
Sent: Friday, July 26, 2019 3:09 PM
To: ██████████████████████████████████████████████
Cc: ██████████████████████████████████████████████>
Subject: Fwd: RE: 31E-MM-108062 victim Report

Hi - I was wondering if you could assist is with the below? in our office and has been assisting us with the victim list?

Is there a way you could pull both lists and have | cross check?

All of your assistance is greatly appreciated!!

<u>Thank</u> you both!

- Type: Forwarded message
- From: [redacted]
- Date: Jul 26, 2019 1:59 PM
- Subject: RE: 31E-MM-108062 victim Report
- To: [redacted]
- Cc: [redacted]
- Key content: "Thank you both! Hi - we have the identified victims in VNS that the case agent has told us to put into vns. You do not need to do anything with VNS."

Hi - we have the identified
… [TRONCATO — originale 4,861 chars]
```

#### Esempio 18 — [SEPARATO] subj: `Re: Fwd: [IP] Search Engine Dispute Notifications: Request For Comments`
*sender: J. Epstein <jeeproject@yahoo.com>*

```
duh


----- Original Message ----
From: Gmax <gmax1@ellmax.com>
To: J. Epstein <jeeproject@yahoo.com>
Sent: Saturday, June 16, 2007 2:17:01 PM
Subject: RE: Fwd: [IP] Search Engine Dispute Notifications: Request For Comments


Cue Verbatim :)


G

PS - my e mail has changed to gmax1@ellmax.com



-----Original Message-----
From: J. Epstein [mailto:jeeproject@yahoo.com]
Sent: Sat 6/16/2007 1:58 PM
To: GMAX1@mindspring.com
Subject: Fw: Fwd: [IP] Search Engine Dispute Notifications: Request For Comments

----- Forwarded Message ----
From: jeffrey epstein <littlestjeff@yahoo.com>
To: me <jeeproject@yahoo.com>
Sent: Saturday, June 16, 2007 1:49:49 PM
Subject: Fw: Fwd: [IP] Search Engine Dispute Notifications: Request For Comments


----- Forwarded Message ----
From: Linda Stone <linda@lindastone.net>
To: littlestjeff@yahoo.com
Sent: Saturday, June 16, 2007 11:50:35 AM
Subject: Fwd: [IP] Search Engine Dispute Notifications: Request For Comments


thought this would be interesting for you to read....

Begin forwarded message:

> From: David Farber <dave@farber.net>
> Date: June 16, 2007 4:05:06 AM PDT
> To: ip@v2.listbox.com
> Subject: [IP] Search Engine Dispute Notifications: Request For Comments
> Reply-To: dave@farber.net
>
>
>
> Begin forwarded message:
>
> From: Lauren Weinstein <lauren@VORTEX.COM>
> Date: June 16, 2007 12:18:39 AM EDT
> To: USACM-INFO@LISTSERV.ACM.ORG
> Subject: Search Engine Dispute Notifications: Request For Comments
> Reply-To: Lauren Weinstein <lauren@VORTEX.COM>
>
>           Search Engine Dispute Notifications: Request For Comments
>
>                 http://lauren.vortex.com/archive/000253.html
>
>
> Greetings.  I'd appreciate feedback from the Internet community
> regarding the following issue.
>
> Search engines have of course become the primary means by which vast
> numbers of people find all manner of information.  For many firms,
> if you don't have a high rank with Google, it's as if you don't
> exist (or at least, many companies appear to feel that way).
>
> Increasingly, cases are appearing of individuals and organizations
> being defamed or otherwise personally damaged -- lives sometimes
> utterly disrupted -- by purpose-built, falsified Web pages,
> frequently located in distant jurisdictions.  Search engine results
> are typically the primary means by which such attacks are promulgated
> and sustained by providing a continuing stream of viewers to those
> Web pages.  Due to ranking algorithms, attempts to counter such
> att
… [TRONCATO — originale 16,452 chars]
```

#### Esempio 19 — [SEPARATO] subj: `Re:`
*sender: Lang, Caroline*

```
Anna would like to apply to USC soon to be able to go there next year in September but she needs to get good grades this year

My parents had a great summer and are in good shape

Le 22 aofit 2018 a 12:36, jeffrey E. <jeevacation@gmail.com> a ecrit :

> yes, very , college decision? mom and dad good?

On Wed, Aug 22, 2018 at 6:00 AM Lang, Caroline wrote:

> Yes ! just came back from vacation
>
> Went in Iceland for a week with some friends and the in Corsica.
>
> And now back to work...
>
> Are you well?

From: jeffrey E. [mailto:jeevacation@gmail.com]
Sent: mardi 21 aotit 2018 18:29
To: Lang, Caroline ce
Subject:

ICAUTIONI

This entail originated outside Warner Bros.

All good??

please note

The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. It is the property of JEE

EFTA01008132

Unauthorized use, disclosure or copying of this communication or any part thereof is strictly prohibited and may be unlawful. If you have received this communication in error, please notify us immediately by return e-mail or by e-mail to jeevacation®gmail.com, and destroy this communication and all copies thereof, including all attachments. copyright -all rights reserved

please note

The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. It is the property of JEE

Unauthorized use, disclosure or copying of this communication or any part thereof is strictly prohibited and may be unlawful. If you have received this communication in error, please notify us immediately by return e-mail or by e-mail to jeevacation®gmail.com, and destroy this communication and all copies thereof, including all attachments. copyright -all rights reserved

EFTA01008133
```

#### Esempio 20 — [SEPARATO] subj: `Fwd: Thank you!`
*sender: jeffrey E.*

```
Forwarded message
From:

>

Date: Thu, Apr 2, 2015 at 3:50 PM

Subject: Thank you!

To: "jeevacation@gmail.com" <jeevacation@gmail.com>

My parents had such a great time at the conservatory! They loved it!!! Thank you so much!!

All the best,

Envoy& de mon iPhone

please note

The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. It is the property of

JEE

Unauthorized use, disclosure or copying of this communication or any part thereof is strictly prohibited and may be unlawful. If you have received this communication in error, please notify us immediately by return e-mail or by e-mail to jeevacation@gmail.com, and destroy this communication and all copies thereof, including all attachments. copyright -all rights reserved

EFTA00860638
```

### Conclusione STEP 1

**Pattern prevalentemente SEPARATI** (100% dei casi): Outlook header e chevron sono blocchi distinti nella stessa email. Il parser deve gestirli come due tipi di blocco separati.

---

## 2a. Body quasi-vuoti con subject Re:/Fwd:

- Email con body < 40 chars E subject Re:/Fwd: nel campione: **710**
- Sotto-campione mostrato: **25** email

### Distribuzione classificazioni (sotto-campione)

| Categoria | N | % |
|-----------|---|---|
| `BREVE_AMBIGUO` | 20 | 80% |
| `QUASI_VUOTO` | 4 | 16% |
| `RISPOSTA_BREVE_LEGITTIMA` | 1 | 4% |

### Body raw (sub-campione 25)

#### Caso 1 — [RISPOSTA_BREVE_LEGITTIMA] subj: `Re:`
```
'great'
```

#### Caso 2 — [BREVE_AMBIGUO] subj: `Re: Linen Place Mats`
```
'grey and white thanks'
```

#### Caso 3 — [QUASI_VUOTO] subj: `Re: Veneer`
```
'yes'
```

#### Caso 4 — [BREVE_AMBIGUO] subj: `Re:`
```
'Sent from my Samsung Galaxy smartphone.'
```

#### Caso 5 — [BREVE_AMBIGUO] subj: `Re: FYI`
```
'Thanks\n\nSent from my iPad'
```

#### Caso 6 — [BREVE_AMBIGUO] subj: `Re:`
```
'Early dinner on Sunday?'
```

#### Caso 7 — [QUASI_VUOTO] subj: `Re: The Daily Beast`
```
'yes'
```

#### Caso 8 — [BREVE_AMBIGUO] subj: `RE: telephone`
```
'HRH The Duke of York KG'
```

#### Caso 9 — [BREVE_AMBIGUO] subj: `Re:`
```
'I know'
```

#### Caso 10 — [BREVE_AMBIGUO] subj: `Re: New AEDs for all the properties`
```
'Thanks Bella, I will do'
```

#### Caso 11 — [QUASI_VUOTO] subj: `Re:`
```
'yes'
```

#### Caso 12 — [BREVE_AMBIGUO] subj: `Re: Gift for Roger Penrose`
```
'please fed ex the gift to roger'
```

#### Caso 13 — [BREVE_AMBIGUO] subj: `Re: Jeffrey Epstein`
```
'Super! Thx\n\nSent from my iPhone'
```

#### Caso 14 — [BREVE_AMBIGUO] subj: `Re: Test`
```
'ali cynthia. cynthia, ali --- g4 sp'
```

#### Caso 15 — [BREVE_AMBIGUO] subj: `Re:`
```
'Now that sounds more like it'
```

#### Caso 16 — [BREVE_AMBIGUO] subj: `Re:`
```
'cool thanks'
```

#### Caso 17 — [BREVE_AMBIGUO] subj: `Fwd: Final =nvoice`
```
'Sent from my =Phone'
```

#### Caso 18 — [QUASI_VUOTO] subj: `Re:`
```
'Yes'
```

#### Caso 19 — [BREVE_AMBIGUO] subj: `Re: Trip`
```
'Hmm. Okay don. Thanks.'
```

#### Caso 20 — [BREVE_AMBIGUO] subj: `Fwd: Fw: The One (1) Question Test…………`
```
'mime part 1.eml'
```

#### Caso 21 — [BREVE_AMBIGUO] subj: `Re:`
```
'Nice'
```

#### Caso 22 — [BREVE_AMBIGUO] subj: `Re: Jeffrey Epstein-we makes st cancel dinner!`
```
'Thank you!\n\nSent from my iPhone'
```

#### Caso 23 — [BREVE_AMBIGUO] subj: `Re: Re: Re:`
```
'Great finaly!\n\nSent from my iPhone'
```

#### Caso 24 — [BREVE_AMBIGUO] subj: `Re: Ion Pictures`
```
'no --make the figures smaller'
```

#### Caso 25 — [BREVE_AMBIGUO] subj: `Re:`
```
'picture 4'
```

### Conclusione STEP 2a

- Risposte brevi legittime (ack/one-liner): ~**84%**
- Body vuoti/quasi-vuoti sospetti (possibile problema estrazione): ~**16%**
- Contenuto presente nonostante body corto: ~**0%**

Implicazione: i body vuoti dopo stripping sono quasi sempre risposte brevi legittime, non artefatti di un parsing fallito. Il parser può restituirli senza marcatura speciale.

---

## 2b. Annidamento profondo (>95° percentile body length)

- 95° percentile lunghezza body: **2,166 chars**
- Email lunghe con segnali di quote: **172**
- Sotto-campione variegato mostrato: **15** email

#### Esempio 1 — depth≈1, body 5,384 chars
*subj: `Fwd: Honeycomb Partners LP: February 2019 Performance Estimate` — contenuto nuovo stimato: 2% [TRASCURABILE (<5%)]*

```
great month for Fiszel...

Richard Kahn
HBRK Associates Inc.
575 Lexington Avenue 4th Floor
New York NY 10022
tel 
fax
cell

Begin forwarded message:

From:
Subject: Honeycomb Partners LP: February 2019 Performance Estimate
Date: March 1, 2019 at 12:55:45 PM EST
To:

CONFIDENTIAL

Dear Investor,

Estimated performance for a representative investor of Honeycomb Master Fund LP is below as of February 28, 2019(a).

| Class "A"    | Month-End   | Year To Date   |
|-|-|-|
| Gross Return | 5.8%        | 11.0%          |
| Net Return   | 4.7%        | 8.8%           |

| Class "Bl"   | Month-End   | Year To Date   |
|-|-|-|
| Gross Return | 5.8%        | 11.1%          |
| Net Return   | 5.0%        | 9.4%           |

EFTA01032084

Please contact

with any questions.

(a) Please note that Honeycomb Master Fund LP includes all or substantially all investible assets from its feeder funds, Honeycomb Partners LP, Honeycomb Intermediate Fund LP and Honeycomb Offshore Fund Ltd. However, investors are expected to invest at the feeder fund not at the master fund level. The reflected returns assume a representative investor invested in Honeycomb Partners LP (the "Fund") in each of (i) the Class A interests that are subject to a management fee of 2% and incentive allocation of 20% per annum and (ii) the Class B1 interests that are subject to a management fee of 1.5% and an incentive allocation of 15% per annum. "Net Return" reflects the performance of the Fund net of management fee, Fund expenses and incentive allocation. "Gross Return" reflects the performance of the Fund net of management fee and Fund expenses, but gross of incentive allocation. Returns assume the reinvestment of all dividends, interest, income and profits. The management fee and Fund expense figures used for performance calculations are pro-rated for the performance period, and incentive allocation calculations reflect an investment in the Fund since its June 1, 2016 inception date. The reflected returns assume 
… [TRONCATO — originale 5,384 chars]
```

#### Esempio 2 — depth≈1, body 2,297 chars
*subj: `Re: Fwd: Gertler Investment/Purchase` — contenuto nuovo stimato: 6% [MINIMO (5-15%)]*

```
ask mort to put in a call to ron burkle who says he
and stephen bing want to buy radar in its entirety

--- DKIESQ@aol.com wrote:

> Please let me know how you wish to proceed.
>  
> Thanks.
>  
> Darren
> > Subject: Gertler Investment/Purchase
> Date: Wed, 21 Dec 2005 12:51:02 -0500
> From: "Alderman, Cyna" <CAlderman@nydailynews.com>
> To: <dkiesq@aol.com>
> CC: "Marcus, Larry" <LMarcus@nydailynews.com>
> 
> Darren-
> 
> Just to follow up on our call yesterday, I am
> waiting to hear back from
> you on Jeffrey's reaction to Eric Gertler's proposal
> to purchase the
> Radar Website.  As discussed, Gertler (who is the
> CEO of Blackbook
> Magazine and Mort Zuckerman's nephew) is proposing
> to purchase the
> assets of MJ LLC relating to the operation of the
> website in exchange
> for stock in KGM, which is a holding company that
> owns Blackbook
> Magazine.  I have not received any diligence
> materials at this time with
> respect to the capital structure of KGM or the value
> of the stock being
> offered, although Gertler has told me that it will
> be $100,000 in
> preferred stock.  I have no way to verify this
> estimation of the value
> of the stock.  Also, as I mentioned to you
> yesterday, Mort Zuckerman is
> currently a minority shareholder in KGM.
> 
> I mentioned to Gertler that we might want to have
> some type of an option
> to unwind the transaction in the event that we are
> able to find a buyer
> for the magazine.  He noted that, although they
> would not commit to any
> print version of Radar, they would consider looking
> for investors in the
> New Year.  It might make sense to include some type
> of payment to MJ LLC
> in the event that Blackbook or any Gertler affiliate
> wanted to proceed
> with the publication of the magazine.  
> 
> Please let me know Jeffrey's thoughts so that I can
> determine if it
> makes sense to draft a purchase agreement at this
> time.
> 
> Thanks-
> 
> Cyna
> 
> 
> Cyna Alderman
> Assistant General Counsel
> Daily News,
… [TRONCATO — originale 2,297 chars]
```

#### Esempio 3 — depth≈1, body 2,319 chars
*subj: `Fwd:` — contenuto nuovo stimato: 1% [TRASCURABILE (<5%)]*

```
Forwarded message
From: Valentino Braitenberg
Date: Wed, Aug 12, 2009 at 11:49 AM
Subject: Re:
To: Jeffrey Epstein <u>leevacationegmail.com></u>

There was a time when anatomy was considered a harmless pastime for shaky old grandfathers, while the young and beautiful stuck electrodes in hying brains and clapped their hands everylime a spike appeared on the face of their oscilloscopes. It was at that time that I started my research and picked neuroanatomy as my main tool, for two reasons: (a) because I did not have the money to buy an oscilloscope and (b) because I was fascinated by the idea of networks being able to do almost anything, as the emerging science of electronic computers seemed to suggest. The new look at brains in terms of information handling networks proved successful in various ways. I am proud of the following:

(1) a very convincing interpretation of the structure of the cerebelum as a time-measuring device with an accuracy of one milisecond or better; (2) an accurate description of a fiber network between the eye and the brain of insects, where each individual fiber is given origin and destination according to a precise scheme derived from geometrical optics; (3) a model of the visual cortex of mammals in complete agreement with the known facts of cortical anatomy and sufficient to explain all the miraculous effects discovered by Hubei and Wiesel, but not explained by them.

Besides these results (1), (2), (3) which were original (and in part even shocking) because of the unusual direct translation of anatomical information into functional schemes, we also did some more conventional neuroanatomy, mainly on the cortex (4), with an emphasis on quantitative relations between number and size of elements, as a necessary contribution to general theories of cortical function (such as Hebb's Cell Assemblies or Moshe Abeles' Synfire Chains).

All told, if you want to know "the most promising part of our work", I think it is a rather relaxed way of theory m
… [TRONCATO — originale 2,319 chars]
```

#### Esempio 4 — depth≈1, body 2,297 chars
*subj: `Re:` — contenuto nuovo stimato: 2% [TRASCURABILE (<5%)]*

```
what day marrakesh? im thinkg of going 18-20

On Mon, Dec 12, 2011 at 9:59 AM, Peter Mandelson < > wrote:

Back in London from Indonesia. Going to HofL. Home this evening. Holidays, going back to Marrakesh. You ? X

From: Jeffrey Epstein [mailto:jeevacation@gmail.com]

Sent: Monday, December 12, 2011 02:31 PM

To: Peter Mandelson

Subject:

Where are you , and what are you going to do for the holidays

*******

The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. It is the property of Jeffrey Epstein

Unauthorized use, disclosure or copying of this communication or any part thereof is strictly prohibited and may be unlawful. If you have received this communication in error, please notify us immediately by return e-mail or by e-mail to jeevacation®gmail.com, and destroy this communication and all copies thereof, including all attachments. copyright -all rights reserved

Disclaimer

This email and any attachments to it may be confidential and are intended solely for the use of the individual to whom it is addressed. My views or opinions expressed are solely those of the author and do not necessarily represent those of Global Counsel LLP. If you are not the intended recipient of this email, you must neither take any action based upon its contents. nor copy or show it to anyone. Please contact the sender if you believe you have received this email in error. Global Counsel LLP is a limited liability partnership registered in England with number OC359787, registered office 27 Farm Street, London W1J SRJ.

**********

The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. It is the property of Jeffrey Epstein

Unauthorized use, disclosure or copying of this communication or any part thereof is strictly prohibited 
… [TRONCATO — originale 2,297 chars]
```

#### Esempio 5 — depth≈1, body 6,701 chars
*subj: `Re: Looking for someone who made the early bet that Middle East would implode...` — contenuto nuovo stimato: 4% [TRASCURABILE (<5%)]*

```
## Jeffrey and Ghislaine: Notes on New York's Oddest Alliance
<http://www.vanityfair.com/online/daily/2011/03/notes-on-new-yorks-oddest-couple-jeffrey-epstein-and-ghislaine-maxwell.html>

by Vicky Ward <http://www.vanityfair.com/contributors/vicky-ward>  
March 8, 2011, 2:30 PM

> "I've got a story idea for you. The rebuilding of Indonesia. Or New Orleans. Or both. Go there. I've just been. You will never think the same way about anything again."

So spoke not Bill or Melinda Gates, but Ghislaine Maxwell, the 48-year-old woman being written up everywhere at the moment as the alleged "procurer" of young women for billionaire Jeffrey Epstein. Epstein, 57, is the financier who spent a year in jail on charges of soliciting prostitutes—and now there is talk of another investigation because various women, now in their twenties and thirties, have come forward with allegations that he molested them when they were under-age. The allegations first surfaced in British newspapers, which have zeroed in on Epstein's friendship with Prince Andrew, who has recently tried to publicly disassociate himself from his old pal.
I wrote a piece for Vanity Fair in 2003 called "The Talented Mr. Epstein." It was largely a business piece that focused on his mysterious exit from Bear Stearns in 1981, his close relationships with Jimmy Cayne, Les Wexner, the chairman of Limited Brands, and above all, the man who claimed to be his mentor, Steven Jude Hoffenberg, who is currently serving a 20-year-jail sentence for bilking investors in Towers Financial out of $450 million.

The piece alluded to Epstein's great friendship with Maxwell, and how she introduced him to young women with whom he had sexual relationships. But, in the end, the story didn't really go there, focusing instead on the issue that remains a mystery—how Jeffrey made his money, and how Ghislaine made hers.

This is not to say I didn't hear stories about the girls. I did. But, not knowing quite who to believe, I concentrated on the 
… [TRONCATO — originale 6,701 chars]
```

#### Esempio 6 — depth≈2, body 4,000 chars
*subj: `Re:` — contenuto nuovo stimato: 1% [TRASCURABILE (<5%)]*

```
and then when asked you LIED ABOUT IT!!!!

On Wed, Jan 17, 2018 at 10:27 PM, wrote:

"taking money for one thing spending itanother and then hiding it". Yes, I took a class after the school [ ]
was already paied. You decided to interpret it in such a sick way. I would have never thought this would cause
such a drama for you. Since I was born I've always had the freedom and the chance to choose whatever classes
I wanted in school ( even if I didn't pay it myself) and I didn't know it would cause such a reaction to you. I'm
sorry for what happened. I apologized many times already

II giomo Thu, Jan 18, 2018 alle 4:04 AM jeffrey E. leevacation@gmail.com> ha scritto: read your excuse for taking money for one thing spending itanother and then hiding it. just more non accpetatnce thta you lie ALL T

he

Forwarded message.
From:
Date: Mon, Jan 15, 2018 at 8:06 PM
Subject: Re:
To: "Jeffrey E." <jeevacation@gmail.com>

Sad to hear that the only thing you care about is your mots. What serious damage did I do to you ? You use the term stealing when the only thing I did was taking a class I was interested in after the semester was already paid. I didn't take any extra money for it. You make it sound like if I robbed you or I don't know what, telling me horrendous things for years, even after I apologized.

What you did to me was much, much worse because you interrupt my studies, left me in the street and all this in the middle of my growth without carrying about my future and all the psychological consequences that followed, including my attachment to you.

I cared about you more than everything and loved you more than anything I have ever seen or imagined and you hurt me greatly treating me like a pair of shoes.

I giomo Mon, Jan 15, 2018 alle 10:43 PM Jeffrey E. leevacation®gmail.com> ha scritto: you take money, - lie, take more - steal take more -lie take more argue- take more lie , and then ask how much i have done TO YOU9999!

On Mon, Jan 15, 2018 at 3:35 PM, [Redacted] < 
… [TRONCATO — originale 4,000 chars]
```

#### Esempio 7 — depth≈2, body 2,183 chars
*subj: `Re: Plane in SAF` — contenuto nuovo stimato: 1% [TRASCURABILE (<5%)]*

```
its up to her

On Sun, May 30, 2010 at 1:29 PM, < > wrote:
Bode says $900 per hour for Cessna 414 twin, same size plane like our C421 was. Its a mid size twin, she can fly left seat and get instruction also,

Sent from my BlackBerry® wireless handheld

From: Jeffrey Epstein <jeevacation@gmail.com>
Date: Sun, 30 May 2010 13:05:19 -0400
To: <
Cc: <
Subject: Re: Plane in SAF

i think a more twin king air, pilatus etc more usefull

On Sun, May 30, 2010 at 12:55 PM, < > wrote:
Jeffrey,
I spoke to Larry at "War Birds" in Santa Fe NM, He owns the training school that flew with a couple of months ago,,,There is a course call "Jet Up Set Recovery", It consists of two flights of 45 - 50 mins, for $3,225.00 plus he also offers acrobatic training in the L39 jet fighter,,,"he said we could do any type of training we like for $2,150.00 per hour,
here is web address: [Redacted]

John Bode is going to send me a message later today on available aircraft at his company also:

Thanks,
Larry

******

**********

The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. It is the property of Jeffrey Epstein Unauthorized use, disclosure or copying of this communication or any part thereof is strictly prohibited and may be unlawful. If you have received this communication in error, please notify us immediately by return e-mail or by e-mail to jeevacation®gmail.com, and destroy this communication and all copies thereof, including all attachments.

EFTA00734994

**********

The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. It is the property of Jeffrey Epstein

Unauthorized use, disclosure or copying of this communication or any part thereof is strictly prohibited and may be unlawful. If you have received this communication in erro
… [TRONCATO — originale 2,183 chars]
```

#### Esempio 8 — depth≈2, body 2,885 chars
*subj: `Fwd: GIV Prebuy update` — contenuto nuovo stimato: 8% [MINIMO (5-15%)]*

```
confirming i am sending deposit (350,000) to escrow account today, although larry references from darren we have two days

Richard Kahn
HBRK Associates Inc.
575 Lexington Avenue, 4th Floor,
New York, New York 10022
tel fax

Begin forwarded message:

From:
Date: March 7, 2013 1:33:46 PM EST
To:
Subject: Fwd: GIV Prebuy update

From:
To:
Sent: 3/7/2013 1:33:13 . Eastern Standard Time
Subj: Re: GIV Prebuy update

yes

On Thu, Mar 7, 2013 at 1:44 PM, < > wrote:
Jeffrey
please confirm, I will sign contract now with corrected dates March 18th no later than April 1st input for prebuy., ***, and Rich is approved to wire $350K to escrow for deposit,. Darren informs that we have two days to apply monies to escrow account when contract is sign by both parties.
is this approved?

thank you,
Larry

In a message dated 3/7/2013 12:32:52 [redacted]. Eastern Standard Time, [redacted] writes:
Yes

On Thursday, March 7, 2013, wrote:
Jeffrey
I met with Dennis, he informed me Mr Taylor is trying to purchase two car dealerships in California and New York, he plans to travel March 22nd - March 29 with his attorney's to close on this deal. This trip is not confirmed since they are still negotiating the terms, firm decision if trip is a go may not come till late next week. Gulfstream has firm input date for March 18th and April 1st reserved for us.
is this acceptable to you? if so Dennis will adjust the contract with these dates and sign contract today.

EFTA00652602

IF we have contract signed, Dennis will allow Gulfstream to start their Log book, AD, and Service bulletin research immediately .

do you accept dates for prebuy input March 18th and April 1st to be included in contract?

thank you,

Larry

wwwww

The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. It is the property of Jeffrey Epstein

Unauthorized use, disclosure or copying of this communicati
… [TRONCATO — originale 2,885 chars]
```

#### Esempio 9 — depth≈2, body 5,425 chars
*subj: `Fw: Follow-up point` — contenuto nuovo stimato: 4% [TRASCURABILE (<5%)]*

```
Ami Sheth | Kirkland & Ellis LLP Citigroup Center |
153 East 53rd Street | New York, NY 10022 |
212-446-4773 Direct | 212-446-6460 Fax |

----- Forwarded by Ami Sheth/New York/Kirkland-Ellis on 08/21/2008 11:27 AM -----

Jay Lefkowitz/New York/Kirkland-Ellis
08/14/2008 04:05 PM

To "Martin Weinberg" <>, Ami Sheth/New York/Kirkland-Ellis@K&E, "Michael Tein"
<>, "Darren " <
cc

Subject Fw: Follow-up point

Marty let's discuss.

From: "Villafana, Ann Marie C. (USAFLS)" [A]
Sent: 08/14/2008 03:27 PM AST
To: Jay Lefkowitz
Cc: "Atkinson, Karen (USAFLS)" < >; "Roy BLACK"
Subject: RE: Follow-up point

Dear Jay:

The modification contained in the December letter is clear and simple, that is why we were not surprised by Mr. Epstein's and his attorneys' actions affirming acceptance of the modification. Mr. Epstein's acceptance of the modification by pleading guilty was equally clear and simple -- it followed written communications from Mr. Sloman and myself that read: "Mr. Epstein has until the close of business on Monday, June 30, 2008, to comply with the terms and conditions of the agreement between the United States and Mr. Epstein (as modified by the U.S. Attorney's December It letter to Ms. Sanchez), including entry of a guilty plea, sentencing, and surrendering to begin his sentence of imprisonment."

As clearly stated in the December letter, only those "individuals whom [the United States] was prepared to name in an Indictment as victims of an enumerated offense" are the beneficiaries of the agreement. That is the list of names that I provided to Messrs. Goldberger and Tein following the change of plea. Under the September/October agreement, all "individuals whom [the United States] has identified as victims" are the beneficiaries, so I would prepare a supplement to the earlier list to include identified victims whom we were not yet prepared to

EFTA00593776

name in an indictment.

Again, as stated in the letter, the modification replaces paragraphs 7 and 8 of the Agre
… [TRONCATO — originale 5,425 chars]
```

#### Esempio 10 — depth≈2, body 4,316 chars
*subj: `Re: Re:` — contenuto nuovo stimato: 4% [TRASCURABILE (<5%)]*

```
Saturday afternoon?

Original Message
From: Jeevacation <jeevacation@gmail.com>
To: Felicia Taylor
Sent: Wed Jul 14 08:55:43 2010
Subject: Re: Re:

Your choice

Sent from my iPhone

On Jul 14, 2010, at 8:54 AM, Felicia Taylor < > wrote:

> Seeing you makes me smile! Saturday, Sunday?
>
> Original Message
• > From: Jeffrey Epstein <jeevacation@gmail.com>
> To: Felicia Taylor
> Sent: Wed Jul 14 07:31:24 2010
> Subject: Re:
>
> of course

>

>

> On Wed, Jul 14, 2010 at 7:30 AM, Felicia Taylor C wrote:

Hey there,
Coming down tomorrow... Have time for a visit over the weekend?
FT

ΑΛΛΛΛΛΛΛ

This email and the information contained herein is confidential and is intended solely for the recipient. Delivery of this email or any of the information contained herein to anyone other than the recipient or his designated representative is unauthorized and any other use, reproduction, distribution or copying of this email or the information contained herein, in whole or in part, without the prior written consent of Hilltop Park Associates LLC or its affiliates is

EFTA00739205

ΑΛΛΛΛΛΛΛΛΛ

>

>

>

>

prohibited. If you have received this message in error, please notify the sender immediately and delete this message and any related attachments.

> The information contained in this communication is > confidential, may be attorney-client privileged, may > constitute inside information, and is intended only for > the use of the addressee. It is the property of > Jeffrey Epstein > Unauthorized use, disclosure or copying of this > communication or any part thereof is strictly prohibited > and may be unlawful. If you have received this > communication in error, please notify us immediately by > return e-mail or by e-mail to jeevacation@gmail.com, and > destroy this communication and all copies thereof, > including all attachments.

• > This email and the information contained herein is confidential and is > intended solely for the recipient. Delivery of this email or any of > the infor
… [TRONCATO — originale 4,316 chars]
```

#### Esempio 11 — depth≈3, body 2,274 chars
*subj: `RE: SDNY investigation` — contenuto nuovo stimato: 11% [MINIMO (5-15%)]*

```
sorry for not giving you a heads up on this. That was not my intent. Just been really busy with a couple ofilMig matters going on now. Please see attached. What media is picking it up? I don't see anything.

» Robert Glassman, Esq.

» Panish Shea & Boyle LLP

>> 11111 Santa Monica Boulevard, Suite 700 Los Angeles, CA 90025

EFTA00090580

>> Tel:

>> Fax

>> Email

>> Web: www.ps aw.com

>> CONFIDENTIALITY NOTICE:

>> This e-mail may contain confidential and privileged material for the sole use of the intended recipient(s). Any review, use, distribution or disclosure by others is strictly prohibited. If you are not the intended recipient (or authorized to receive for the recipient), please contact the sender by reply e-mail or telephone, and delete all copies of this message.

>> If you are a potential client, the information you disclose to us by email will be kept in strict confidence and will be protected to the full extent of the law. Please be advised, however, that Panish Shea & Boyle LLP and its lawyers do not represent you until you have signed a retainer agreement with the firm. Until that time, you are responsible for any statutes of limitations or other deadlines for your case or potential case. >> >> -----Original Message----- >> From: >>[mailto: >> Sent: Friday, January 17, 2020 4:52 PM >> To: Robert Glassman >> Cc: >; Nathan Werksman >>>

>> Subject: RE: SDNY investigation

>>

>> Robert,

>>>

>> Based on media reports today it looks like you filed the civil lawsuit? I don't think we realized that was imminent -- could we ask you to please send us a copy of the filing? I don't yet see it on PACER. >> >> thanks, >> -----Original Message----- >> From: >> Sent: Monday, December 30, 2019 22:28 >> To: Robert Glassman >> Cc: >> >; Nathan Werksman < >> Subject: RE: SDNY investigation

>>

>> Great, thanks very much. We'll likely start with siblings and mother and then go from there. As soon as we have a sense of when it would be productive for us to return fo
… [TRONCATO — originale 2,274 chars]
```

#### Esempio 12 — depth≈3, body 2,227 chars
*subj: `Fwd:` — contenuto nuovo stimato: 1% [TRASCURABILE (<5%)]*

```
Forwarded message
From: jeffrey E. <jeevacation@gmail.com>
Date: Mon, Sep 15, 2014 at 2:10 PM
Subject: Re:
To: Larry Summers

great

On Mon, Sep 15, 2014 at 2:09 PM, Larry Summers cza wrote: On Monday.

Sent from my iPad

Please direct all scheduling inquiries to my office

Follow me on twitter @lhsummers

On Sep 14, 2014, at 8:10 PM, "jeffrey E." <jeevacation@gmail.com> wrote:

are you in week of 21?

please note

The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. It is the property of JEE

Unauthorized use, disclosure or copying of this communication or any part thereof is strictly prohibited and may be unlawful. If you have received this communication in error, please notify us immediately by return e-mail or by e-mail to jea@gmail.com, and destroy this communication and all copies thereof, including all attachments. copyright -all rights reserved

please note

EFTA00996943

The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. It is the property of JEE

Unauthorized use, disclosure or copying of this communication or any part thereof is strictly prohibited and may be unlawful. If you have received this communication in error, please notify us immediately by return e-mail or by e-mail to jeevacation@gmail.com, and destroy this communication and all copies thereof, including all attachments. copyright -all rights reserved

please note

The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. It is the property of JEE

Unauthorized use, disclosure or copying of this communication or any part thereof is strictly prohibited and may be unlawful. If you have received this communic
… [TRONCATO — originale 2,227 chars]
```

#### Esempio 13 — depth≈3, body 2,325 chars
*subj: `Re:` — contenuto nuovo stimato: 8% [MINIMO (5-15%)]*

```
They came and I think they had a really good time. They were also happy to meet Mizuka for the first time... and finding out that she was pregnant. I told you that already right?

> On Dec 24, 2016, at 1:02 PM, Jeffrey E. <jeevacation@gmail.com> wrote: > > and brockmans? > On Sat, Dec 24, 2016 at 12:22 PM, Joi Ito -al > wrote: > Lots of people but lots of fun. Max Tegmark and I were talking about how it was fun because we "mixed it up" (Harvard doesn't recommend inviting non-faculty to faculty events.) He said that he was at an event where he told the table he was a plumber and no one talked to him. I told him that my plumber was actually at our party. :-) > > Probably not enough structured conversation to have been much fun for you though. It was mostly about lots of food and alcohol. > > How's Palm Beach? > > BTW, let me know when you decide when Karyna is going to Japan. > > - Joi > >> On Dec 24, 2016, at 10:25 AM, jeffrey E. <jeevacation@gmail.com> wrote: > > » how was last night? > > > > -- » please note >>> The information contained in this communication is >>> confidential, may be attorney-client privileged, may >>> constitute inside information, and is intended only for > > the use of the addressee. It is the property of > > JEE > > Unauthorized use, disclosure or copying of this > > communication or any part thereof is strictly prohibited > > and may be unlawful. If you have received this >> communication in error, please notify us immediately by >> return e-mail or by e-mail to jeevacation@gmail.com, and > > destroy this communication and all copies thereof, > > including all attachments. copyright -all rights reserved > -- > please note

EFTA01058618

> The information contained in this communication is

> confidential, may be attorney-client privileged, may

> constitute inside information, and is intended only for

> the use of the addressee. It is the property of

> JEE

> Unauthorized use, disclosure or copying of this

> communication or any part the
… [TRONCATO — originale 2,325 chars]
```

#### Esempio 14 — depth≈3, body 5,863 chars
*subj: `Re: Travel arrangements for [Redacted] traveling on 01/24/2014` — contenuto nuovo stimato: 0% [TRASCURABILE (<5%)]*

```
thx

On Jan 21, 2014, at 11:20 AM, [REDACTED] < [REDACTED] > wrote:

I

Sent from my iPhone

On Jan 21, 2014, at 11:06 AM, [REDACTED] > wrote:

HI ...here is your ticket back to NY this Friday, Jan. 24th
Jojo, please pick up from the airport and take her back to 301. confirm back to me please!

Begin forwarded message:

From: "American Express Travel" <AmericanExpressTravel@trondent.com>
Subject: Travel arrangements for traveling on 01/24/2014
Date: January 21, 2014 11:04:46 AM EST
To:

DO NOT REPLY TO THIS EMAIL. This message was sent from a notification only address that cannot accept incoming messages. If you have any questions, please contact Centurion Travel Service at 1-877- 877-0987.

Your travel arrangements are outlined below in the email. Please refer to attached PDF attachment and itinerary for more details regarding your travel arrangements. Your Centurion Travel Service travel plans have been posted to a secure website. Please click on the link to view your trip details: https://www.aeairweb.com/Mytravelarrangements/index.jsp

If airline tickets are purchased for this itinerary: Airline Baggage Fee/Rules may apply and can be accessed by visiting: https://www.aeairweb.com/Mytravelarrangements/Airline BaggagePolicies.jsp

First time user? Refer to instructions when accessing the above website. Enter your email address and temporary password to gain access to the website. You will receive your temporary password in a separate email.

Record Locator:
Traveler:

EFTA00375766

Flight Information:
Reserved: DELTA AIR LINES 676
Class: Coach
Seats: 23A
Departs: St Thomas, VIRGIN ISLANDS - STT
Date: Jan 24,2014 Time: 2:48 PM
Arrives: New York JFK, NY - JFK
Date: Jan 24,2014 Time: 6:00 PM

Airline Confirmation Numbers:

DELTA AIR LINES

NEED PASSPORT OR VISA SERVICES?

As a service to our customers, American Express has partnered with VisaCentral for visa and passport services.

To learn what documents may be required for your international destination, or to obta
… [TRONCATO — originale 5,863 chars]
```

#### Esempio 15 — depth≈3, body 2,556 chars
*subj: `Re: Inspiration New York e-vite` — contenuto nuovo stimato: 2% [TRASCURABILE (<5%)]*

```
we will try now to scheudl woody, hardeep, metre on sun or monday

On Fri, Jun 6, 2014 at 3:02 AM, █████████████████████ wrote:

Do you still wish to purchase 2 tickets to the Amfar event?

Sent from my iPhone

Begin forwarded message:

From: Boris Nikolic
Date: June 5, 2014, 10:56:59 PM EDT
To:
Ce: Richard Kahn
Subject: RE: Inspiration New York e-vite

Can you please check with Jee if still wants to go.

I just found out something about that event that might be a turn off for him.

I sent him an email re that.

Please check and let me know!

If he is still for go — I will reach out re tickets.

B

From: Lesley Groff <mailto:lesley.ieetagmail.conli>
Sent: Thursday, June 5, 2014 1:05 PM
To: Boris Nikolic
Cc: Richard Kahn
Subject: Re: Inspiration New York e-vite

EFTA_R1_00362958
EFTA01920054

Hi Boris...can you let me know what level ticket you have? Jeffrey would like us to purchase 2 tickets for him but he wants to be at the same level so he can sit with you...Please let me know as soon as possible :) thanks,

On May 30, 2014, at 10:29 AM, Boris Nikolic <████████████████████ wrote:

HI Lesley

The info re AMFAR event is below.

It is June 10th!

lee did not get back to me.

See you soon

B

From: Zackary Hemenway <mailto:>
Sent: Thursday, May 15, 2014 1:20 PM
To: Boris Nikolic
Subject: Inspiration New York e-vite

Hi Boris:

Thank you for helping us make the Inspiration Gala New York come together. We are very excited for the event and couldn't have done it without you.

EFTA_R1_00362959
EFTA01920055

I wanted to send the e-vite to you so you can share with your circle of friends in case there was anyone else who would be interested in purchasing a ticket or table.

See attached for the e-vite and below for a link to purchase online.

https://www.kintera.org/AutoGen/Register/] K9PQLkLVK9PYKeKSIdP3

Best,

Zack Hemenway
Josh Wood Productions
www.joshwoodproductions.com

<INNY-EVITE-10B.jpg>

please note

The information contained in this communication is confidentia
… [TRONCATO — originale 2,556 chars]
```

### Conclusione STEP 2b

- Contenuto nuovo mediano sul sotto-campione: **2%** del body totale
- Trascurabile (<5%): 11/15 email
- Minimo (5-15%): 4/15 email
- Significativo (>15%): 0/15 email

---

## 3. Implicazioni per il Parser

> Proposte basate sui dati osservati. Non implementare prima di approvazione umana (AGENTS.md §2).

### 3.1 OUTLOOK_HEADER_BLOCK vs CHEVRON_QUOTE: un tipo o due?

**Proposta: trattarli come DUE tipi distinti di blocco quotato.**

Motivazione: i pattern si presentano frequentemente come blocchi separati nella stessa email. Il parser deve rilevare entrambi: prima un eventuale blocco chevron, poi un eventuale blocco Outlook inline (senza '>').

### 3.2 Body vuoti dopo stripping: ignorare o preservare?

**Proposta: preservare i body vuoti/brevi come risultato legittimo**, senza fallback né comportamento speciale.

Motivazione: il ~84% dei casi sono risposte brevi legittime (ack, one-liner). Il corpo vuoto è il contenuto reale del messaggio, non un artefatto. Restituire stringa vuota (o quasi vuota) con `has_thread=True` è il comportamento corretto: segnala che l'unico contenuto era una risposta minima.

### 3.3 Profondità di annidamento: seguire tutti i livelli o cappare?

**Proposta: estrarre SOLO il primo livello (il messaggio corrente), senza seguire ricorsivamente la catena.**

Motivazione: il contenuto nuovo nei body profondi è mediano al 2% del body totale. Quello che interessa all'embedding è solo il testo scritto dal mittente corrente: tutto ciò che viene dopo il primo marker di quote è 'storia' della catena e introduce ridondanza semantica. Approccio: trovare il primo occorrenza di qualsiasi pattern di quote (ON_DATE_WROTE, chevron, Original Message, Begin forwarded) e troncare lì. Restituire il testo prima del primo marker come `content_new`, e tutto il resto come `thread_tail` (opzionale, per analisi forensi).

Eccezione: se `content_new` è vuoto o < 10 chars, non applicare lo strip e restituire il body intero — safe-by-default come per il disclaimer.
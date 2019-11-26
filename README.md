# AI_X tech blog
***

# Project Title : naïve bayes classifier를 이용하여 게임 ‘리그 오브 레전드’의 아군 챔피언(캐릭터) 선택에 따른 챔피언 추천 

***

## Members
* 박철우
* 이윤지
* 이동한
* 이제환

***

## Table of Contents
* [1.Introduction](#chapter-1)
* [2.DataSets](#chapter-2)
* [3.Methodology](#chapter-3)
* [4.Evaluate & Analysis](#chapter-4)
* [5.Related Work](#chapter-5)
* [6.Conclusion](#chapter-6)

***

<a id="chapter-1"></a>
### 1.Introduction
‘리그 오브 레전드’는 미국의 라이엇 게임즈가 개발 및 서비스 중인 MOBA(Multiplayer Online Battle Arena)장르의 게임으로, 현재 전세계적으로 가장 인기 있는 PC 온라인 게임 중 하나이다. ‘리그 오브 레전드’ 에서는 비슷한 점수대의 유저들이 선호 포지션에 따른 Random으로 선택된 10명의 유저들이 5vs5로 대전하는 게임이며, 각각의 유저들은 게임에서 사용할 챔피언(캐릭터)를 선택한다. 선택할 수 있는 챔피언은 총 145개가 존재하며 각각의 챔피언은 모두 서로 다른 능력치와 스킬을 가지기 때문에 어떤 챔피언을 고르는 지에 따라 게임의 승패에 큰 영향을 미치게 된다. 또한 챔피언들은 같은 팀으로 선택되었을 때 서로가 가진 특징에 따라 상승효과를 불러 일으키는 경우가 많기 때문에 챔피언을 고를 때에는 아군 혹은 적군이 어떤 챔피언을 고르는지도 챔피언 선택의 중요한 근거가 될 수 있다. 우리는 naïve bayes classifier를 이용하여 다른 아군 4명이 챔피언을 골랐을 때 어떤 챔피언을 고르는 것이 승률이 높을 것인지를 근거로 선택할 챔피언을 추천하고자 한다.

<a id="chapter-2"></a>
### 2.DataSets
‘리그 오브 레전드’에서는 자체 API를 통해 게임 플레이 데이터를 제공하고 있다. https://developer.riotgames.com/ 사이트를 통해 API 사용 신청하여 승인을 받았고, 이를 통해 naïve bayes classifier (혹은 다른 알고리즘)를 수행하는 데 충분한 데이터를 얻을 수 있다.

데이터 수집 방법 : ‘리그 오브 레전드’에서는 자체 API를 통해 게임 플레이 데이터를 제공하고 있다. https://developer.riotgames.com/ 사이트를 통해 API 사용 신청하여 승인을 받았고, 이를 통해 naïve bayes classifier (혹은 다른 알고리즘)를 수행하는 데 충분한 데이터를 얻을 수 있다.

데이터 예:
1) Game id를 구한뒤에 해당 game id로 RIOT API를 이용해 해당 게임에 대한 모든 정보를 불러옴


```"participants": [
224)	        {
225)	            "spell1Id": 14,
226)	            "participantId": 1,
227)	            "timeline": {
228)	                "lane": "BOTTOM",
229)	                "participantId": 1,
230)	                "csDiffPerMinDeltas": {
231)	                    "30-end": 2.6999999999999997,
232)	                    "20-30": 1.3499999999999999,
233)	                    "0-10": -1.4500000000000002,
234)	                    "10-20": 0.49999999999999956
235)	                },
236)	                "goldPerMinDeltas": {
237)	                    "30-end": 299.6,
238)	                    "20-30": 365.8,
239)	                    "0-10": 174.2,
240)	                    "10-20": 287
241)	                },
242)	                "xpDiffPerMinDeltas": {
243)	                    "30-end": 183.00000000000006,
244)	                    "20-30": 12.099999999999994,
245)	                    "0-10": -2.0500000000000114,
246)	                    "10-20": 33.650000000000006
247)	                },
248)	                "creepsPerMinDeltas": {
249)	                    "30-end": 2.2,
250)	                    "20-30": 2.3,
251)	                    "0-10": 0.2,
252)	                    "10-20": 0.8999999999999999
253)	                },
254)	                "xpPerMinDeltas": {
255)	                    "30-end": 390,
256)	                    "20-30": 358.6,
257)	                    "0-10": 291.1,
258)	                    "10-20": 385.6
259)	                },
260)	                "role": "DUO_SUPPORT",
261)	                "damageTakenDiffPerMinDeltas": {
262)	                    "30-end": -216.80000000000007,
263)	                    "20-30": -213.60000000000008,
264)	                    "0-10": -76.95,
265)	                    "10-20": -287.54999999999995
266)	                },
267)	                "damageTakenPerMinDeltas": {
268)	                    "30-end": 365.8,
269)	                    "20-30": 487.3,
270)	                    "0-10": 120.60000000000001,
271)	                    "10-20": 122.2
272)	                }
273)	            },
274)	            "spell2Id": 4,
275)	            "teamId": 100,
276)	            "stats": {
277)	                "neutralMinionsKilledTeamJungle": 0,
278)	                "visionScore": 65,
279)	                "magicDamageDealtToChampions": 26636,
280)	                "largestMultiKill": 1,
281)	                "totalTimeCrowdControlDealt": 31,
282)	                "longestTimeSpentLiving": 1283,
283)	                "perk1Var1": 250,
284)	                "perk1Var3": 0,
285)	                "perk1Var2": 994,
286)	                "tripleKills": 0,
287)	                "perk5": 8313,
288)	                "perk4": 8347,
289)	                "playerScore9": 0,
290)	                "playerScore8": 0,
291)	                "kills": 5,
292)	                "playerScore1": 0,
293)	                "playerScore0": 0,
294)	                "playerScore3": 0,
295)	                "playerScore2": 0,
296)	                "playerScore5": 0,
297)	                "playerScore4": 0,
298)	                "playerScore7": 0,
299)	                "playerScore6": 0,
300)	                "perk5Var1": 0,
301)	                "perk5Var3": 0,
302)	                "perk5Var2": 0,
303)	                "totalScoreRank": 0,
304)	                "neutralMinionsKilled": 0,
305)	                "statPerk1": 5008,
306)	                "statPerk0": 5008,
307)	                "damageDealtToTurrets": 2043,
308)	                "physicalDamageDealtToChampions": 1792,
309)	                "damageDealtToObjectives": 3745,
310)	                "perk2Var2": 0,
311)	                "perk2Var3": 0,
312)	                "totalUnitsHealed": 1,
313)	                "perk2Var1": 0,
314)	                "perk4Var1": 0,
315)	                "totalDamageTaken": 9164,
316)	                "perk4Var3": 0,
317)	                "wardsKilled": 4,
318)	                "largestCriticalStrike": 0,
319)	                "largestKillingSpree": 2,
320)	                "quadraKills": 0,
321)	                "magicDamageDealt": 63767,
322)	                "firstBloodAssist": false,
323)	                "item2": 3151,
324)	                "item3": 3020,
325)	                "item0": 3157,
326)	                "item1": 3853,
327)	                "item6": 3364,
328)	                "item4": 3285,
329)	                "item5": 0,
330)	                "perk1": 8226,
331)	                "perk0": 8229,
332)	                "perk3": 8237,
333)	                "perk2": 8210,
334)	                "perk3Var3": 0,
335)	                "perk3Var2": 0,
336)	                "perk3Var1": 690,
337)	                "damageSelfMitigated": 5599,
338)	                "magicalDamageTaken": 3227,
339)	                "perk0Var2": 0,
340)	                "firstInhibitorKill": false,
341)	                "trueDamageTaken": 217,
342)	                "assists": 17,
343)	                "perk4Var2": 0,
344)	                "goldSpent": 10550,
345)	                "trueDamageDealt": 788,
346)	                "participantId": 1,
347)	                "physicalDamageDealt": 3337,
348)	                "sightWardsBoughtInGame": 0,
349)	                "totalDamageDealtToChampions": 29216,
350)	                "physicalDamageTaken": 5719,
351)	                "totalPlayerScore": 0,
352)	                "win": true,
353)	                "objectivePlayerScore": 0,
354)	                "totalDamageDealt": 67893,
355)	                "neutralMinionsKilledEnemyJungle": 0,
356)	                "deaths": 3,
357)	                "wardsPlaced": 28,
358)	                "perkPrimaryStyle": 8200,
359)	                "perkSubStyle": 8300,
360)	                "turretKills": 1,
361)	                "firstBloodKill": false,
362)	                "trueDamageDealtToChampions": 788,
363)	                "goldEarned": 12068,
364)	                "killingSprees": 2,
365)	                "unrealKills": 0,
366)	                "firstTowerAssist": false,
367)	                "firstTowerKill": false,
368)	                "champLevel": 15,
369)	                "doubleKills": 0,
370)	                "inhibitorKills": 0,
371)	                "firstInhibitorAssist": false,
372)	                "perk0Var1": 1829,
373)	                "combatPlayerScore": 0,
374)	                "perk0Var3": 0,
375)	                "visionWardsBoughtInGame": 0,
376)	                "pentaKills": 0,
377)	                "totalHeal": 502,
378)	                "totalMinionsKilled": 48,
379)	                "timeCCingOthers": 18,
380)	                "statPerk2": 5002
381)	            },
382)	            "championId": 63
383)	        },
384)	        {
385)	            "spell1Id": 14,
386)	            "participantId": 2,
387)	            "timeline": {
388)	                "lane": "JUNGLE",
389)	                "participantId": 2,
390)	                "goldPerMinDeltas": {
391)	                    "30-end": 440.4,
392)	                    "20-30": 365.7,
393)	                    "0-10": 200.8,
394)	                    "10-20": 267.6
395)	                },
396)	                "creepsPerMinDeltas": {
397)	                    "30-end": 5,
398)	                    "20-30": 7,
399)	                    "0-10": 5.1,
400)	                    "10-20": 6
401)	                },
402)	                "xpPerMinDeltas": {
403)	                    "30-end": 538.8,
404)	                    "20-30": 510.1,
405)	                    "0-10": 359.70000000000005,
406)	                    "10-20": 472.09999999999997
407)	                },
408)	                "role": "NONE",
409)	                "damageTakenPerMinDeltas": {
410)	                    "30-end": 335.8,
411)	                    "20-30": 412.70000000000005,
412)	                    "0-10": 373,
413)	                    "10-20": 404.59999999999997
414)	                }
415)	            },
416)	            "spell2Id": 4,
417)	            "teamId": 100,
418)	            "stats": {
419)	                "neutralMinionsKilledTeamJungle": 5,
420)	                "visionScore": 27,
421)	                "magicDamageDealtToChampions": 192,
422)	                "largestMultiKill": 1,
423)	                "totalTimeCrowdControlDealt": 121,
424)	                "longestTimeSpentLiving": 1128,
425)	                "perk1Var1": 722,
426)	                "perk1Var3": 0,
427)	                "perk1Var2": 200,
428)	                "tripleKills": 0,
429)	                "perk5": 8451,
430)	                "perk4": 8473,
431)	                "playerScore9": 0,
432)	                "playerScore8": 0,
433)	                "kills": 2,
434)	                "playerScore1": 0,
435)	                "playerScore0": 0,
436)	                "playerScore3": 0,
437)	                "playerScore2": 0,
438)	                "playerScore5": 0,
439)	                "playerScore4": 0,
440)	                "playerScore7": 0,
441)	                "playerScore6": 0,
442)	                "perk5Var1": 205,
443)	                "perk5Var3": 0,
444)	                "perk5Var2": 0,
445)	                "totalScoreRank": 0,
446)	                "neutralMinionsKilled": 9,
447)	                "statPerk1": 5008,
448)	                "statPerk0": 5005,
449)	                "damageDealtToTurrets": 7339,
450)	                "physicalDamageDealtToChampions": 17194,
451)	                "damageDealtToObjectives": 8561,
452)	                "perk2Var2": 10,
453)	                "perk2Var3": 0,
454)	                "totalUnitsHealed": 1,
455)	                "perk2Var1": 21,
456)	                "perk4Var1": 530,
457)	                "totalDamageTaken": 15499,
458)	                "perk4Var3": 0,
459)	                "wardsKilled": 1,
460)	                "largestCriticalStrike": 569,
461)	                "largestKillingSpree": 2,
462)	                "quadraKills": 0,
463)	                "magicDamageDealt": 192,
464)	                "firstBloodAssist": false,
465)	                "item2": 3031,
466)	                "item3": 2055,
467)	                "item0": 3153,
468)	                "item1": 3006,
469)	                "item6": 3364,
470)	                "item4": 3046,
471)	                "item5": 0,
472)	                "perk1": 9111,
473)	                "perk0": 8005,
474)	                "perk3": 8014,
475)	                "perk2": 9104,
476)	                "perk3Var3": 0,
477)	                "perk3Var2": 0,
478)	                "perk3Var1": 416,
479)	                "damageSelfMitigated": 8817,
480)	                "magicalDamageTaken": 4477,
481)	                "perk0Var2": 846,
482)	                "firstInhibitorKill": false,
483)	                "trueDamageTaken": 864,
484)	                "assists": 8,
485)	                "perk4Var2": 0,
486)	                "goldSpent": 11275,
487)	                "trueDamageDealt": 13585,
488)	                "participantId": 2,
489)	                "physicalDamageDealt": 156539,
490)	                "sightWardsBoughtInGame": 0,
491)	                "totalDamageDealtToChampions": 17556,
492)	                "physicalDamageTaken": 10157,
493)	                "totalPlayerScore": 0,
494)	                "win": true,
495)	                "objectivePlayerScore": 0,
496)	                "totalDamageDealt": 170317,
497)	                "neutralMinionsKilledEnemyJungle": 0,
498)	                "deaths": 3,
499)	                "wardsPlaced": 14,
500)	                "perkPrimaryStyle": 8000,
501)	                "perkSubStyle": 8400,
502)	                "turretKills": 1,
503)	                "firstBloodKill": false,
504)	                "trueDamageDealtToChampions": 170,
505)	                "goldEarned": 12250,
506)	                "killingSprees": 1,
507)	                "unrealKills": 0,
508)	                "firstTowerAssist": false,
509)	                "firstTowerKill": false,
510)	                "champLevel": 17,
511)	                "doubleKills": 0,
512)	                "inhibitorKills": 0,
513)	                "firstInhibitorAssist": false,
514)	                "perk0Var1": 1619,
515)	                "combatPlayerScore": 0,
516)	                "perk0Var3": 773,
517)	                "visionWardsBoughtInGame": 5,
518)	                "pentaKills": 0,
519)	                "totalHeal": 1630,
520)	                "totalMinionsKilled": 208,
521)	                "timeCCingOthers": 19,
522)	                "statPerk2": 5002
523)	            },
524)	            "championId": 133
525)	        },
526)	        {
527)	            "spell1Id": 7,
528)	            "participantId": 3,
529)	            "timeline": {
530)	                "lane": "BOTTOM",
531)	                "participantId": 3,
532)	                "csDiffPerMinDeltas": {
533)	                    "30-end": 2.6999999999999997,
534)	                    "20-30": 1.3499999999999999,
535)	                    "0-10": -1.4500000000000002,
536)	                    "10-20": 0.49999999999999956
537)	                },
538)	                "goldPerMinDeltas": {
539)	                    "30-end": 548.4,
540)	                    "20-30": 416.79999999999995,
541)	                    "0-10": 222.7,
542)	                    "10-20": 371.7
543)	                },
544)	                "xpDiffPerMinDeltas": {
545)	                    "30-end": 183.00000000000006,
546)	                    "20-30": 12.099999999999994,
547)	                    "0-10": -2.0500000000000114,
548)	                    "10-20": 33.650000000000006
549)	                },
550)	                "creepsPerMinDeltas": {
551)	                    "30-end": 8,
552)	                    "20-30": 4.4,
553)	                    "0-10": 5.3,
554)	                    "10-20": 6.199999999999999
555)	                },
556)	                "xpPerMinDeltas": {
557)	                    "30-end": 729.4,
558)	                    "20-30": 434.8,
559)	                    "0-10": 312.20000000000005,
560)	                    "10-20": 409.8
561)	                },
562)	                "role": "DUO_CARRY",
563)	                "damageTakenDiffPerMinDeltas": {
564)	                    "30-end": -216.80000000000007,
565)	                    "20-30": -213.60000000000008,
566)	                    "0-10": -76.95,
567)	                    "10-20": -287.54999999999995
568)	                },
569)	                "damageTakenPerMinDeltas": {
570)	                    "30-end": 605,
571)	                    "20-30": 661.3,
572)	                    "0-10": 170.5,
573)	                    "10-20": 389.5
574)	                }
575)	            },
576)	            "spell2Id": 4,
577)	            "teamId": 100,
578)	            "stats": {
579)	                "neutralMinionsKilledTeamJungle": 21,
580)	                "visionScore": 26,
581)	                "magicDamageDealtToChampions": 6264,
582)	                "largestMultiKill": 2,
583)	                "totalTimeCrowdControlDealt": 37,
584)	                "longestTimeSpentLiving": 1018,
585)	                "perk1Var1": 422,
586)	                "perk1Var3": 0,
587)	                "perk1Var2": 340,
588)	                "tripleKills": 0,
589)	                "perk5": 8236,
590)	                "perk4": 8226,
591)	                "playerScore9": 0,
592)	                "playerScore8": 0,
593)	                "kills": 5,
594)	                "playerScore1": 0,
595)	                "playerScore0": 0,
596)	                "playerScore3": 0,
597)	                "playerScore2": 0,
598)	                "playerScore5": 0,
599)	                "playerScore4": 0,
600)	                "playerScore7": 0,
601)	                "playerScore6": 0,
602)	                "perk5Var1": 48,
603)	                "perk5Var3": 0,
604)	                "perk5Var2": 0,
605)	                "totalScoreRank": 0,
606)	                "neutralMinionsKilled": 28,
607)	                "statPerk1": 5008,
608)	                "statPerk0": 5005,
609)	                "damageDealtToTurrets": 7937,
610)	                "physicalDamageDealtToChampions": 8848,
611)	                "damageDealtToObjectives": 14566,
612)	                "perk2Var2": 0,
613)	                "perk2Var3": 0,
614)	                "totalUnitsHealed": 4,
615)	                "perk2Var1": 27,
616)	                "perk4Var1": 250,
617)	                "totalDamageTaken": 16622,
618)	                "perk4Var3": 0,
619)	                "wardsKilled": 2,
620)	                "largestCriticalStrike": 403,
621)	                "largestKillingSpree": 2,
622)	                "quadraKills": 0,
623)	                "magicDamageDealt": 37807,
624)	                "firstBloodAssist": false,
625)	                "item2": 3124,
626)	                "item3": 3006,
627)	                "item0": 3115,
628)	                "item1": 3157,
629)	                "item6": 3340,
630)	                "item4": 3042,
631)	                "item5": 0,
632)	                "perk1": 9111,
633)	                "perk0": 8005,
634)	                "perk3": 8014,
635)	                "perk2": 9103,
636)	                "perk3Var3": 0,
637)	                "perk3Var2": 0,
638)	                "perk3Var1": 531,
639)	                "damageSelfMitigated": 10782,
640)	                "magicalDamageTaken": 5229,
641)	                "perk0Var2": 731,
642)	                "firstInhibitorKill": true,
643)	                "trueDamageTaken": 300,
644)	                "assists": 12,
645)	                "perk4Var2": 284,
646)	                "goldSpent": 14045,
647)	                "trueDamageDealt": 15857,
648)	                "participantId": 3,
649)	                "physicalDamageDealt": 145207,
650)	                "sightWardsBoughtInGame": 0,
651)	                "totalDamageDealtToChampions": 15398,
652)	                "physicalDamageTaken": 11093,
653)	                "totalPlayerScore": 0,
654)	                "win": true,
655)	                "objectivePlayerScore": 0,
656)	                "totalDamageDealt": 198872,
657)	                "neutralMinionsKilledEnemyJungle": 0,
658)	                "deaths": 4,
659)	                "wardsPlaced": 11,
660)	                "perkPrimaryStyle": 8000,
661)	                "perkSubStyle": 8200,
662)	                "turretKills": 0,
663)	                "firstBloodKill": false,
664)	                "trueDamageDealtToChampions": 286,
665)	                "goldEarned": 14273,
666)	                "killingSprees": 2,
667)	                "unrealKills": 0,
668)	                "firstTowerAssist": false,
669)	                "firstTowerKill": false,
670)	                "champLevel": 17,
671)	                "doubleKills": 1,
672)	                "inhibitorKills": 1,
673)	                "firstInhibitorAssist": false,
674)	                "perk0Var1": 1225,
675)	                "combatPlayerScore": 0,
676)	                "perk0Var3": 493,
677)	                "visionWardsBoughtInGame": 1,
678)	                "pentaKills": 0,
679)	                "totalHeal": 3185,
680)	                "totalMinionsKilled": 204,
681)	                "timeCCingOthers": 1,
682)	                "statPerk2": 5002
683)	            },
684)	            "championId": 145
685)	        },
686)	        {
687)	            "spell1Id": 7,
688)	            "participantId": 4,
689)	            "timeline": {
690)	                "lane": "MIDDLE",
691)	                "participantId": 4,
692)	                "csDiffPerMinDeltas": {
693)	                    "30-end": -0.8000000000000003,
694)	                    "20-30": -4.5,
695)	                    "0-10": 0.10000000000000053,
696)	                    "10-20": 2.2
697)	                },
698)	                "goldPerMinDeltas": {
699)	                    "30-end": 488.8,
700)	                    "20-30": 303.6,
701)	                    "0-10": 271.6,
702)	                    "10-20": 378.4
703)	                },
704)	                "xpDiffPerMinDeltas": {
705)	                    "30-end": 281.4,
706)	                    "20-30": -194.60000000000002,
707)	                    "0-10": -3.4000000000000057,
708)	                    "10-20": 56.299999999999955
709)	                },
710)	                "creepsPerMinDeltas": {
711)	                    "30-end": 3.4,
712)	                    "20-30": 3.1999999999999997,
713)	                    "0-10": 7.2,
714)	                    "10-20": 8.1
715)	                },
716)	                "xpPerMinDeltas": {
717)	                    "30-end": 657.4,
718)	                    "20-30": 319.5,
719)	                    "0-10": 463.6,
720)	                    "10-20": 499
721)	                },
722)	                "role": "SOLO",
723)	                "damageTakenDiffPerMinDeltas": {
724)	                    "30-end": -675.8,
725)	                    "20-30": -541.5999999999999,
726)	                    "0-10": -190.89999999999998,
727)	                    "10-20": -182.20000000000002
728)	                },
729)	                "damageTakenPerMinDeltas": {
730)	                    "30-end": 206.2,
731)	                    "20-30": 480.6,
732)	                    "0-10": 95.1,
733)	                    "10-20": 254
734)	                }
735)	            },
736)	            "spell2Id": 4,
737)	            "teamId": 100,
738)	            "stats": {
739)	                "neutralMinionsKilledTeamJungle": 0,
740)	                "visionScore": 17,
741)	                "magicDamageDealtToChampions": 31276,
742)	                "largestMultiKill": 1,
743)	                "totalTimeCrowdControlDealt": 205,
744)	                "longestTimeSpentLiving": 1188,
745)	                "perk1Var1": 1060,
746)	                "perk1Var3": 0,
747)	                "perk1Var2": 0,
748)	                "tripleKills": 0,
749)	                "perk5": 8014,
750)	                "perk4": 8009,
751)	                "playerScore9": 0,
752)	                "playerScore8": 0,
753)	                "kills": 6,
754)	                "playerScore1": 0,
755)	                "playerScore0": 0,
756)	                "playerScore3": 0,
757)	                "playerScore2": 0,
758)	                "playerScore5": 0,
759)	                "playerScore4": 0,
760)	                "playerScore7
```


여기서 우리가 사용할것은 ‘participants’ key값을 가진 데이터만 뽑아서 사용함. 그중 Champion Id 값을 이용해 각 플레이어가 어떤 챔피언을 골랐는지 알 수 있음.

<a id="chapter-3"></a>
### 3.Methodology

naïve bayes classifier 소개 : naïve bayes classifier는 조건부 확률에 대한 bayes theorem에 기반한 것으로 조건부 확률 P(C_i│x_1,⋯x_p )를 계산하게 되며 C_i는 해당 레코드가 속하게 되는 클래스,즉 이 문제에서는 승리 혹은 패배가 되며, 범주형 예측 변수인 x_1,⋯x_p는 아군 5명 각각이 선택한 챔피언이 된다.

<a id="chapter-4"></a>
### 4.Evaluation & Analysis

...준비중...

<a id="chapter-5"></a>
### 5.Related Work

...준비중...

<a id="chapter-6"></a>
### 6. Conclusion

...준비중...
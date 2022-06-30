def help_command(text): 

	if '날씨' in text:
		help_message = str([
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "날씨 명령어에 대해 알려드릴께요!\n *멈뭄미 날씨* 라고 입력하면 멈뭄미가 날씨를 알려준답니다!\n 메시지는 아래와 같이 생겼어요."
				}
			},
			{
				"type": "divider"
			},
			{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": "오늘 날씨를 알려드릴께요."
				}
			},
			{
				"type": "context",
				"elements": [
					{
						"type": "mrkdwn",
						"text": "서울특별시 ○○구"
					}
				]
			},
			{
				"type": "section",
				"fields": [
					{
						"type": "plain_text",
						"text": "날씨 : 하루종일 맑음"
					},
					{
						"type": "plain_text",
						"text": "미세먼지 : 좋음 (10㎍/㎥)"
					},
					{
						"type": "plain_text",
						"text": "온도 : 10.00°C ~ 10.00°C"
					},
					{
						"type": "plain_text",
						"text": "초미세먼지 : 좋음 (10㎍/㎥)"
					},
					{
						"type": "plain_text",
						"text": "체감온도 : 10.00°C ~ 10.00°C"
					},
					{
						"type": "plain_text",
						"text": "강수확률 : 50%"
					},
					{
						"type": "plain_text",
						"text": "습도 : 50.0%"
					},
					{
						"type": "plain_text",
						"text": "강수량 : 1.0mm"
					}
				],
				"accessory": {
					"type": "image",
					"image_url": "https://ssl.gstatic.com/onebox/weather/64/sunny.png",
					"alt_text": "plants"
				}
			},
			{
				"type": "divider"
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "추가로 사용할 수 있는 옵션은 지역과 시간이 있어요!"
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "지역의 경우 메시지에 지역을 추가하면 되요! \n'멈뭄미 날씨 강남' 과 같은 식으로 사용 가능합니다!\n시간의 경우 오늘, 내일, 모레, 주간이 있고, '멈뭄미 날씨 내일'과 같은 식으로 사용 가능합니다. "
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "혹여나 멈뭄미가 틀릴 수 있는데 ~그건 기상청의 잘못입니다~"
				}
			}
		])
	elif '문서' in text or '찾기' in text:
		help_message = str([
			{
				"type": "section",
				"text": { 
					"type": "mrkdwn",
					"text": "아직 이 기능의 도움말이 제작되지 않았습니다."
				}
			}
		])
	elif '탈잉' in text or '접속' in text:
		help_message = str([
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "아직 이 기능의 도움말이 제작되지 않았습니다."
				}
			}
		])
	elif '메뉴' in text or '점심' in text or '배고파' in text:
		help_message = str([
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "아직 이 기능의 도움말이 제작되지 않았습니다."
				}
			}
		])
	else:
		help_message = str([
			{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": "안녕하세요. 멈뭄미 봇이에요~ :laughing::laughing:\n 사용 가능한 명령어는 아래와 같아요!\n"
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "명령어를 사용하실 땐 꼭 앞에 *멈뭄미* 를 붙여주셔야해요!\n일정시간동안 요청이 없으면 수면모드로 전환되며 이때 답장이 조금 지연될 수 있습니다."
				}
			},
			{
				"type": "divider"
			},
			{
				"type": "section",
				"fields": [
					{
						"type": "mrkdwn",
						"text": "*날씨*\n현재 날씨를 멈뭄미가 알려줘요!\n ex) 멈뭄미 날씨\nex) 멈뭄미 강남구 날씨\n."
					},
					{
						"type": "mrkdwn",
						"text": "*문서찾기*\n멈뭄미가 문서를 찾아줘요!\nex) 멈뭄미 문서 도서신청\nex) 멈뭄미 찾기 전체회의\n."
					},
					{
						"type": "mrkdwn",
						"text": "*탈잉 접속자 수*\n현재 탈잉 페이지에 접속자수를 \n볼 수 있어요!\nex) 멈뭄미 탈잉\nex) 멈뭄미 접속자"
					},
					{
						"type": "mrkdwn",
						"text": "*메뉴 선택*\n멈뭄미가 식사 메뉴를 추천해줘요!\nex) 멈뭄미 점심\nex) 멈뭄미 배고파\nex) 멈뭄미 식사"
					},
					{
						"type": "mrkdwn",
						"text": ".\n*명령어*\n멈뭄미의 명령어를 볼 수 있어요! \nex) 멈뭄미 명령어\nex) 멈뭄미 도움말\nex) 멈뭄미 help \n.\n."
					},
					{
						"type": "mrkdwn",
						"text": ".\n*명령어 상세보기*\n해당 명령의 기능을 상세히 볼 수 있어요! \nex) 멈뭄미 도움말 문서\nex) 멈뭄미 help 날씨\nex) 멈뭄미 도움말 날씨\n."
					}
				]
			},
			{
				"type": "divider"
			},
			
			{
				"type": "context",
				"elements": [
					{
						"type": "mrkdwn",
						"text": "Last updated: 01 03, 2020"
					}
				]
			}
		])
	return help_message
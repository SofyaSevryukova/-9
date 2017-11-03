<head>
	<title> News </title>
	<link href="static/style.css" rel="stylesheet" type="text/css" />
</head>
<body>
	<div id="header">
		<h1>News agregator</h2>
		<h3>Неразмеченых статей: {{len(rows)}}</h3>
	</div>
	
	<div id="main">
		<div class = "titleParent">
			<div class="titleT" style="background-color: #0099CC; font-size: 15pt; color: #f9f9f9;">Title</div>
			<div class="date" style="background-color: #0099CC; font-size: 15pt; color: #f9f9f9;">Date</div>
			<div class="labelT" style="background-color: #0099CC; font-size: 15pt; color: #f9f9f9;">Label</div>
		</div>
		%if len(rows) == 0:
			<div id = "nonews">
				No news loaded! <br>
				<h3>Click button below to load some</h3>				
			</div>
		%end
		%for row in rows:
			<div class="newsBlock">
				<div class="title"><a href="{{row.url}}">{{row.title}}</a></div>
				<div class = "date">{{row.date}}</div>
				%if row.predict == "good":
					<div class="labelG" style="background-color: #33FF66;"> <a href="/add_label?label=good&id={{row.id}}">Интересно</a></div>		
					<div class="labelM"> <a href="/add_label?label=maybe&id={{row.id}}">Возможно</a></div>
					<div class="labelN"> <a href="/add_label?label=never&id={{row.id}}">Не интересно</a></div>					
				%elif row.predict == "maybe":
					<div class="labelG"> <a href="/add_label?label=good&id={{row.id}}">Интересно</a></div>		
					<div class="labelM" style="background-color: #FF9933;"> <a href="/add_label?label=maybe&id={{row.id}}">Возможно</a></div>
					<div class="labelN"> <a href="/add_label?label=never&id={{row.id}}">Не интересно</a></div>	
				%elif row.predict == "never":
					<div class="labelG"> <a href="/add_label?label=good&id={{row.id}}">Интересно</a></div>		
					<div class="labelM"> <a href="/add_label?label=maybe&id={{row.id}}">Возможно</a></div>
					<div class="labelN" style="background-color: #FF3300;"> <a href="/add_label?label=never&id={{row.id}}">Не интересно</a></div>		
				%else:
					<div class="labelG"> <a href="/add_label?label=good&id={{row.id}}">Интересно</a></div>		
					<div class="labelM"> <a href="/add_label?label=maybe&id={{row.id}}">Возможно</a></div>
					<div class="labelN"> <a href="/add_label?label=never&id={{row.id}}">Не интересно</a></div>	
				%end
			</div>
		%end
	</div>
	
	<div id="MoreNews">
		<a href="/update_news" class="flatBtn">I WANNA MORE TECH NEWS!!</a>
	<!-- 	<a href="/load_all" class="loadAllBtn">LOAD 100</a> -->
		<!--<a href="/train" class="flatBtn" style="background-color: #CCCCCC; color: black;">TRAIN</a>-->
	</div>
	
	<div id ="footer">
		<div class="floorUp"></div>
		<h2>Created by Sevryukova</h2>
		<h3>2017</h3>
	</div>
</body>
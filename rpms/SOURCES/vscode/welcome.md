<div class="welcome-doc">


<div class="header">
	<div class="logo"></div>
	<h1>Hello, welcome to Visual Studio Code!</h1>
	<p>Here are four topics to get you up and running</p>
</div>

<div class="tips">
    <div class="tip">
	    <div class="content">
		    <h3>Take a quick tour</h3>
		    <p>Get instantly productive by <a href="http://go.microsoft.com/fwlink/?LinkID=536379#VSCode" target="_blank">learning the basics</a> of Code.  Once completed, move onto <a href="http://go.microsoft.com/fwlink/?LinkID=533484#VSCode" target="_blank">our full set of docs</a> to become a Code master.</p>
	</div>
    </div>
	<div class="tip">
		<div class="content">
		    <h3>Start building apps today</h3>
			<p>Our step-by-step guides will get you going quickly so you can experience the enhanced support we offer for <a href="http://go.microsoft.com/fwlink/?LinkID=533693#VSCode" target="_blank">Node.js</a> and <a href="http://go.microsoft.com/fwlink/?LinkID=533692#VSCode" target="_blank">ASP.NET 5</a>.</p>
		</div>
	</div>
	<div class="tip">
		<div class="content">
		    <h3>Install extensions</h3>
			<p>Find hundreds of useful extensions in the <a href="https://marketplace.visualstudio.com/" target="_blank">marketplace</a> to enhance your coding environment.</p>
		</div>
	</div>
</div>
<div class="tips">
	<div class="tip">
		<div class="content">
		    <h3>Task running and Git</h3>
		    <p>Code can participate in your existing development workflow with integrated <a href="http://go.microsoft.com/fwlink/?LinkId=613691#VSCode" target="_blank">task running</a> and <a href="http://go.microsoft.com/fwlink/?LinkID=533695#VSCode" target="_blank">Git support</a>.</p>
		</div>
    </div>
	<div class="tip">
		<div class="content">
		    <h3>Debugging, IntelliSense and more</h3>
		    <p>See the level of support Code includes for various <a href="http://go.microsoft.com/fwlink/?LinkID=533691#VSCode" target="_blank">programming languages</a>, including those with an <a href="http://go.microsoft.com/fwlink/?LinkID=533689#VSCode" target="_blank">evolved editing</a> experience (IntelliSense, Peek Definition, ...) and <a href="http://go.microsoft.com/fwlink/?LinkID=533694#VSCode" target="_blank">debugging</a>.</p>
		</div>
    </div>
</div>

<style>
.welcome-doc * {
	box-sizing: border-box;
}

.welcome-doc {
	font-size: 13px;	
}

.vs .welcome-doc {
	color: #6F6F6F;
}

.vs-dark .welcome-doc {
	color: #CCC;	
}

.vs-dark .welcome-doc a {
	color: #39F;	
}

.welcome-doc h1 {
	font-family: 'Segoe UI Light', 'Segoe UI', 'SFUIDisplay-Thin', 'HelveticaNeue-Thin', 'HelveticaNeue-Light', 'Helvetica Neue Light', 'Helvetica Neue', Helvetica, sans-serif;
	font-weight: 300;
	font-size: 24px;
	margin-bottom: 0;
}

.vs .welcome-doc h1 {
	color: #373277;	
}

.vs-dark .welcome-doc h1 {
	color: #B5A0FF;	
}

.welcome-doc h3 {
	font-size: 14px;
	font-weight: normal;
}

.welcome-doc ul {
	list-style: none;
	padding: 0;
}

.welcome-doc ul > li {
	margin-bottom: 6px;
}

.vs .welcome-doc h2,
.vs .welcome-doc h3,
.vs .welcome-doc strong {
	color: #1E1E1E;	
}

.vs-dark .welcome-doc h2,
.vs-dark .welcome-doc h3,
.vs-dark .welcome-doc strong {
	color: #F1F1F1;	
}

.welcome-doc .header {
	width: 90%;
	max-width: 675px;
	text-align: center;
	margin: 10% auto 30px;
}

.welcome-doc .header > * {
	text-align: left;	
}

.welcome-doc .logo {
	height: 64px;
	width: 64px;
	opacity: 0.1;
}

.vs .welcome-doc .logo {
	background: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyOCIgaGVpZ2h0PSIyOSI+PHBhdGggZmlsbD0iIzAwMCIgZD0iTTIxIDBsLTExIDEyLTcuMzMzLTUuNjY2LTIuNjY3IDEuNjgydjEzLjk4NGwyLjY2NyAxLjY2NiA3LjMzMy01LjY2NiAxMSAxMSA3LTN2LTIyLjMzM2wtNy0zLjY2N3ptLTE4IDE5di05bDQgNS00IDR6bTExLTRsNy02djEybC03LTZ6Ii8+PC9zdmc+") left center no-repeat;
	background-size: contain;
}

.vs-dark .welcome-doc .logo {
	background: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyOCIgaGVpZ2h0PSIyOSI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTIxIDBsLTExIDEyLTcuMzMzLTUuNjY2LTIuNjY3IDEuNjgydjEzLjk4NGwyLjY2NyAxLjY2NiA3LjMzMy01LjY2NiAxMSAxMSA3LTN2LTIyLjMzM2wtNy0zLjY2N3ptLTE4IDE5di05bDQgNS00IDR6bTExLTRsNy02djEybC03LTZ6Ii8+PC9zdmc+") left center no-repeat;
	background-size: contain;
}

.welcome-doc .header p {
	margin-top: 10px;	
}

.welcome-doc .tips {
	margin: 20px auto;
	width: 90%;
	max-width: 675px;
}

.welcome-doc .tips .tip {
	float: left;
	vertical-align: top;
	width: 50%;
	margin-bottom: 12px;	
	padding-right: 15px;
	text-align: left;	
}

.welcome-doc .tips .tip:before {
	content: "";	
	height: 0;
	width: 64px;
	border-top: 2px solid #BBB;
	display: block;
}

.vs-dark .welcome-doc .tips .tip:before {	
	border-color: #666;	
}

.welcome-doc .tips:after,
.welcome-doc .tips .tip:after {
	clear: both;
	content: '';
	display: block;
	visibility: hidden;
	height: 0;
}

.welcome-doc .tips .tip > * {
	float: left;
}

.welcome-doc .tip .content {
	width: 100%;
	padding-top: 20px;
	line-height: 1.4;
}

.welcome-doc .tip .content p,
.welcome-doc .tip .content h3 {
	margin: 0;
}

.welcome-doc .getting-started {
	margin-top: 36px;	
}

@media screen and (min-width: 480px) {
	.welcome-doc .tips .tip {	
		padding-right: 30px;
	}
}

@media screen and (min-width: 675px) {
	.welcome-doc {
		font-size: 14px;
	}
	
	.welcome-doc .header,
	.welcome-doc .tips {
		width: 85%;	
	}
	
	.welcome-doc h1 {
		font-size: 32px;
	}
	
	.welcome-doc h3 {
		font-size: 18px;
	}
}
</style>

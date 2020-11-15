# coding: utf-8
import os
import pandas as pd
import json

"""
This helper renders chat conversations passed as a json dump of a dictionary:
    --conversation contact id/name
        --num message (start from 0 each time is fine)
            --data-name = correspondant (phone or ID)
            --data-time = time of message (formatted as str)
            --from_me = (boolean - 0 = received / 1 = sent)
            --message = message content

example:
    {
        "Vincent":{
            "0":{
                "data-name": "Vincent",
                "data-time": "2020-11-10 08:00:00",
                "from_me" : 0,
                "Message": "What is your favorite tool?"
            },
            "1":{
                "data-name": "Vincent",
                "data-time": "2020-11-10 08:01:00",
                "from_me" : 1,
                "Message": "iLEAPP !"
            },
        },
        "Mike,Vincent":{
            "0":{
                "data-name": "Mike",
                "data-time": "2020-11-10 08:08:00",
                "from_me" : 0,
                "Message": "Who like apples ?"
            },
            "1":{
                "data-name": "Vincent",
                "data-time": "2020-11-10 08:09:00",
                "from_me" : 1,
                "Message": "I do!"
            }
    }

"""

CSS="""
<style>
@import url(https://fonts.googleapis.com/css?family=Lato:400,700);
*, *:before, *:after {
  box-sizing: border-box;
}

body {
  background: rgba(255, 255, 255, 0.1);
  font: 14px/20px "Lato", Arial, sans-serif;
  padding: 10px 0;
  color: white;
}

li{
  list-style-type: none;
}

.container {
  margin: 0 auto;
  width: 750px;
  background: #444753;
  border-radius: 5px;
}

.people-list {
  width: 260px;
  float: left;
}

.people-list .search {
  padding: 20px;
}

.people-list input {
  border-radius: 3px;
  border: none;
  padding: 14px;
  color: white;
  background: #6A6C75;
  width: 90%;
  font-size: 14px;
}

.people-list .fa-search {
  position: relative;
  left: -25px;
}

.people-list ul {
  padding: 20px;
  //height: 770px;
  list-style-type: none;
}

.people-list ul li {
  padding-bottom: 20px;
}

.people-list li:hover {
  background: rgba(255, 255, 255, 0.25);
}

.people-list .active {
  background: rgba(255, 255, 255, 0.25);
}

.people-list img {
  float: left;
}

.people-list .about {
  float: left;
  margin-top: 8px;
  padding-left: 8px;
}

.chat {
  width: 490px;
  float: left;
  background: #F2F5F8;
  border-top-right-radius: 5px;
  border-bottom-right-radius: 5px;
  color: #434651;
}

.chat .chat-header {
  padding: 20px;
  border-bottom: 2px solid white;
}

.chat .chat-header img {
  float: left;
}
.chat .chat-header .chat-about {
  float: left;
  padding-left: 10px;
  margin-top: 6px;
}

.chat .chat-header .chat-with {
  font-weight: bold;
  font-size: 16px;
}

.chat .chat-header .chat-num-messages {
  color: #92959E;
}

.chat .chat-history {
  padding: 30px 30px 20px;
  border-bottom: 2px solid white;
  overflow-y: scroll;
}

.chat .chat-history .message-data {
  margin-bottom: 15px;
}

.chat .chat-history .message-data-time {
  color: #a8aab1;
  padding-left: 6px;
}

.chat .chat-history .message {
  color: white;
  padding: 18px 20px;
  line-height: 26px;
  font-size: 16px;
  border-radius: 7px;
  margin-bottom: 30px;
  width: 90%;
  position: relative;
}

.chat .chat-history .message:after {
  bottom: 100%;
  left: 7%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
  border-bottom-color: #86BB71;
  border-width: 10px;
  margin-left: -10px;
}

.chat .chat-history .my-message {
  background: #86BB71;
}

.chat .chat-history .other-message {
  background: #94C2ED;
}

.chat .chat-history .other-message:after {
  border-bottom-color: #94C2ED;
  left: 93%;
}

.me {
  margin-right: 3px;
  font-size: 10px;
}

.me {
  color: #94C2ED;
}

.align-left {
  text-align: left;
}

.align-right {
  text-align: right;
}

.float-right {
  float: right;
}

.clearfix:after {
  visibility: hidden;
  display: block;
  font-size: 0;
  content: " ";
  clear: both;
  height: 0;
}

</style>

"""

includes = """
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
"""

chat_HTML = """
<div class="container clearfix">
    <div class="people-list" id="people-list">
      <ul class="list" id="list">

      </ul>
    </div>
    <div class="chat">
      <div class="chat-header clearfix">


        <div class="chat-about">
          <div class="chat-with" id="chat-with">Click on the left to view messages</div>
          <div class="chat-num-messages" id="chat-num-messages"></div>
        </div>
      </div> <!-- end chat-header -->
      <div id="chat-history" class="chat-history">
      </div>
    </div>
</div>
<br />
<br />
"""

js = """
<script type="text/javascript">
function createDivMessages (m){

    var messType = '<div class="message my-message">';
    var liTag = '<li>';
    var messDataTag = '<div class="message-data">';
    var name = m["data-name"];

    if (m["from_me"] == 1) {
        messType = '<div class="message other-message float-right">';
        liTag = '<li class="clearfix">'
        messDataTag = '<div class="message-data align-right">';
        name = "Me";
    }

    var res = liTag;
    res += messDataTag;
    res += '<span class="message-data-time" >';
    res += m["data-time"];
    res += '</span> &nbsp; &nbsp;';
    res += '<span class="message-data-name" >';
    res += name;
    res += '</span>';
    res += '</div>';
    res += messType;
    res += m["body_to_render"];
    res += '</div>';
    res += '</li>';

    return res;
}

function showHistory (messages, name){

    html = "<ul>";
    for (let m in messages){
      html += createDivMessages(messages[m], name);
    }
    html += "</ul>";
    $("#chat-history").html(html);
    return false;
}

function createPeopleList(list){

    var res = '';
    for (let p in list){
        res += '<li class="clearfix" id="';
        res += list[p];
        res += '">';
        res +=  '<div class="about">';
        res +=    '<div class="name">';
        res += list[p];
        res += '</div>';
        res +=  '</div>';
        res += '</li>';
    }
    $("#list").html(res);
}

function updateHeader(name, num){
    $("#chat-with").html(name);
    $("#chat-num-messages").html("Total: "+num)
    return false;
}

$(document).ready(function() {
    var messages = JSON.parse(json);

    createPeopleList(Object.keys(messages));

    $('.people-list li').click(function(){
        $(this).addClass('active').siblings().removeClass('active');
        var id = $(this).attr('id');
        showHistory(messages[id]);
        updateHeader(id,Object.keys(messages[id]).length);
        return false;
    });
});
</script>
"""

mimeTypeIcon = {
    "image":"📷",
    "audio":"🎧",
    "video":"🎥",
    "animated":"🎡",
    "application":"📎",
}

"""
format JS to include in report html
"""
def render_js_chat(chat_json):
    json_js = """
    <script type="text/javascript">
     var json = {0!r};
    </script>
    """.format(chat_json)
    return '\n'.join([json_js,js])

"""
helper to render body with attachments
"""
def integrateAtt(rec):
    if rec["file-path"]:
        att_type = rec["content-type"].split('/')[0] if rec["content-type"] else 'application'
        filename = os.path.basename(rec["file-path"])
        body = rec["message"] if rec["message"] else ''
        if att_type == 'image':
            source = '<img src="{}" width="256" height="256"/>'.format(rec["file-path"])

        elif att_type == 'audio':
            source = """
            <audio controls>
              <source src="{0}" type="{1}">
              <p><a href="{0}"></a> </p>
            </audio>
            """.format(rec["file-path"],rec["content-type"])
        elif att_type == 'video':
            source = """
            <video controls width="256">
              <source src="{0}" type="{1}">
              <p><a href="{0}"></a> </p>
            </video>
            """.format(rec["file-path"],rec["content-type"])
        else:
            source = '<a href="{}">{}</a>'.format(rec["file-path"],filename)

        return "\n".join([body,mimeTypeIcon[att_type]+' '+source])
    else:
        return rec["message"]


"""
transform a chat df to be rendered to js
input : df with following columns:
    - data-name str : contact name / number
    - data-time dt : time of message (needs to be datetime format)
    - message str : text message
    - content-type str : mime type of atachement or None (ex : 'image/jpeg')
    - file-path str : path of attachment to render
    - from_me bool : 0 if received, 1 if sent
output :
    str including script and data to include in report html

"""
def render_chat(df):
    df["body_to_render"] = df.apply(lambda rec: integrateAtt(rec),axis=1)
    latest_mess = df.groupby("data-name", as_index=False)["data-time"].max()
    df = df.merge(latest_mess, on=["data-name"], how='right', suffixes=["","_latest"]).sort_values(by=['data-time_latest','data-name'], ascending=[False, True])
    df["data-time"] = df["data-time"].dt.strftime('%Y-%m-%d %H:%M:%S')
    chats = {}
    for c in df["data-name"].unique():
        chats[c]=df[df["data-name"] == c][["data-name","from_me","body_to_render","data-time"]].reset_index(drop=True).to_dict(orient='index')

    json_chat = json.dumps(chats)
    return render_js_chat(json_chat)
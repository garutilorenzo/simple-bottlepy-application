<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    % title = post.title if defined('post') else ''
    % meta = get_meta(page_name=page_name, title=title)
    <meta name="description" content="{{ meta.description }}">
    <meta name="author" content="Lorenzo Garuti">
    <title>{{ meta.title }}</title>

    <link rel="canonical" href="{{ url() }}">
    <link rel="icon" href="/static/img/bottle.ico" />
    

    <!-- Bootstrap core CSS -->
    <link href="/static/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="/static/navbar-top-fixed.css" rel="stylesheet">
    <link href="/static/custom.css" rel="stylesheet">
  </head>
  <body>
  % include('nav.tpl')
package com.jxdevelopment.neno.client;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.RootPanel;
import com.jxdevelopment.neno.client.Discussions;

/**
 * Entry point classes define <code>onModuleLoad()</code>.
 */
public class DiscussionViewer implements EntryPoint {
	public void onModuleLoad() {
		Discussions discussionPanel = new Discussions();
		discussionPanel.show();
	}
}

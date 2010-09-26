package com.jxdevelopment.neno.client;

import com.extjs.gxt.ui.client.Style.Orientation;
import com.extjs.gxt.ui.client.widget.Window;
import com.extjs.gxt.ui.client.widget.layout.RowLayout;
import com.extjs.gxt.ui.client.widget.layout.BorderLayout;
import com.google.gwt.user.client.ui.HorizontalSplitPanel;
import com.extjs.gxt.ui.client.widget.layout.BorderLayoutData;
import com.extjs.gxt.ui.client.Style.LayoutRegion;
import com.google.gwt.user.client.ui.DecoratorPanel;
import com.google.gwt.user.client.ui.DecoratedTabPanel;
import com.extjs.gxt.ui.client.widget.TabPanel;
import com.extjs.gxt.ui.client.widget.TabItem;
import com.extjs.gxt.ui.client.widget.LayoutContainer;
import java.util.Collections;
import com.extjs.gxt.ui.client.widget.layout.FillLayout;
import com.extjs.gxt.ui.client.widget.layout.FitLayout;
import com.extjs.gxt.ui.client.widget.ContentPanel;
import com.extjs.gxt.ui.client.widget.toolbar.ToolBar;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.TextField;
import com.extjs.gxt.ui.client.widget.toolbar.FillToolItem;
import com.extjs.gxt.ui.client.widget.form.DateField;
import com.extjs.gxt.ui.client.widget.HtmlContainer;
import com.extjs.gxt.ui.client.widget.ListView;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.layout.CardLayout;
import com.extjs.gxt.ui.client.widget.form.SimpleComboBox;

public class Discussions extends Window {

	public Discussions() {
		// Window config
		setSize("760", "570");
		setHeading("neno");
		setLayout(new BorderLayout());
		
		// Home tab panel
		TabPanel tabPanel = new TabPanel();		
		TabItem homeTab = getHomeTabPanel();
		tabPanel.add(homeTab);
		
		// Empty discussion panel, for testing purposes
		TabItem discussionListPanel = getDiscussionTabPanel("Discussion");
		tabPanel.add(discussionListPanel);
		
		add(tabPanel, new BorderLayoutData(LayoutRegion.CENTER));

		// Navigation panel
		ContentPanel cntntpnlDiscussions = getDiscussionsCardPanel();
		ContentPanel discussionsPanel = getDiscussionsPanel();
		cntntpnlDiscussions.add(discussionsPanel);
		
		add(cntntpnlDiscussions, new BorderLayoutData(LayoutRegion.WEST, 240.0f));
	}

	/**
	 * @return ContentPanel
	 */
	public ContentPanel getDiscussionsCardPanel() {
		ContentPanel cntntpnlDiscussions = new ContentPanel();
		cntntpnlDiscussions.setHeaderVisible(false);
		cntntpnlDiscussions.setHeading("Discussions");
		cntntpnlDiscussions.setCollapsible(true);
		
		ToolBar discussionSelectionTB = new ToolBar();
		
		// Add board button
		Button btnNewBoard = new Button("Add Board");
		discussionSelectionTB.add(btnNewBoard);
		
		FillToolItem fillToolItem = new FillToolItem();
		discussionSelectionTB.add(fillToolItem);
		
		// Board selection combo
		SimpleComboBox smplcmbxBoard = new SimpleComboBox();
		smplcmbxBoard.setAllowBlank(false);
		smplcmbxBoard.setEditable(false);
		smplcmbxBoard.setForceSelection(true);
		smplcmbxBoard.setName("boardSelection");
		smplcmbxBoard.setFieldLabel("Board");
		discussionSelectionTB.add(smplcmbxBoard);		

		// Add top toolbar
		cntntpnlDiscussions.setTopComponent(discussionSelectionTB);
		cntntpnlDiscussions.setLayout(new CardLayout());
		
		return cntntpnlDiscussions;
	}

	/**
	 * @return
	 */
	public TabItem getHomeTabPanel() {
		TabItem homeTab = new TabItem("Home");
		homeTab.setLayout(new FitLayout());
		
		HtmlContainer htmlContainer = new HtmlContainer("<h1>neno</h1>\n<p>Welcome to <b>neno</b>!</p>\n<p>Browse forums by adding their feeds using the \"Add Board\" button in the left panel.</p>\n<p>Clicking on a discussion topic in the list will open up a new tab in this panel showing all posts in that discussion.</p>");
		homeTab.add(htmlContainer);
		return homeTab;
	}

	/**
	 * @param String
	 * @return TabItem
	 */
	public TabItem getDiscussionTabPanel(String title) {
		TabItem discussionListPanel = new TabItem(title);
		
		ListView listView = new ListView(new ListStore());
		listView.setTemplate("<table>\n<tpl for=\".\">\n<tr>\n<td class=\"nenoPostSubject\" colspan=\"3\">\n{subject}\n</td>\n</tr>\n<tr>\n<td class=\"nenoPostIcon\">{icon.image}</td>\n<td class=\"nenoPostAuthor\">{author.name}</td>\n<td class=\"nenoPostCreated\">{created}</td>\n</tr>\n<tr>\n<td class=\"nenoPostBody\" colspan=\"3\">\n{display_body}\n</td>\n</tr>\n</tpl>\n</table>");
		discussionListPanel.add(listView);
		return discussionListPanel;
	}

	/**
	 * @return ContentPanel
	 */
	public ContentPanel getDiscussionsPanel() {
		ContentPanel discussionsPanel = new ContentPanel();
		discussionsPanel.setHeaderVisible(true);
		discussionsPanel.setHeading("Discussions");
		discussionsPanel.setCollapsible(false);
		discussionsPanel.setLayout(new FitLayout());
		
		ListView listView = new ListView(new ListStore());
		discussionsPanel.add(listView);
		listView.setTemplate("<table>\n<tpl for=\".\">\n<tr class=\"nenoTopicRow\">\n<td class=\"nenoSubject\">{subject}</td>\n<td class=\"nenoAuthor\">{author}</td>\n<td class=\"nenoCreated\">{created}</td>\n</tr>\n<tr>\n<td colspan=\"3\" class=\"nenoSlug\">{slug}</td>\n</tr>\n</tpl>\n</table>");
		
		ToolBar discussionFilterTB = new ToolBar();
		
		// Discussion text filter field
		TextField txtfldFilter = new TextField();
		discussionFilterTB.add(txtfldFilter);
		txtfldFilter.setWidth("100");
		txtfldFilter.setName("filterDiscussions");
		txtfldFilter.setWidth(130);
		txtfldFilter.setSelectOnFocus(true);
		txtfldFilter.setFieldLabel("Filter");
		
		// Discussion date filter field
		DateField dtfldDate = new DateField();
		discussionFilterTB.add(dtfldDate);
		dtfldDate.setWidth("");
		dtfldDate.setName("dateFilter");
		dtfldDate.setWidth(100);
		dtfldDate.setFieldLabel("Date");
		
		discussionsPanel.setTopComponent(discussionFilterTB);
		
		return discussionsPanel;
	}

}

def plot_fig_age(ses_df, sense, age_group_vals, y_ticks, annotation_offset):
    """
    Visualize (highly structured, see below) ses_df across the intersection of blindness/deafness and age group.

    ses_df is
    """
    vis_fig2_df = ses_df[ses_df['Cond_Category_R1'] == sense]
    dis_order = ['age_1', 'age_2', 'age_3', 'age_4']
    #LEGEND
    name_to_color = {
        '18-44':   (0.534313725490196, 0.7519607843137255, 0.534313725490196, 1),
        '45-64':   (0.7480392156862745, 0.7009803921568627, 0.8127450980392157, 1),
        '65-74':   (0.9338235294117646, 0.7544117647058823, 0.5838235294117647, 1),
        '≥ 75':    (1.        , 1.        , 0.6       , .9)
    }


    tup_list = []
    for r in include_race_eth:
        #for s in ['Poor', 'Near poor', 'Not poor']:
        for a in dis_order:
            tup_list.append([r, a])

    person_counts = []
    for i in tup_list:
        count = vis_fig2_df[(vis_fig2_df["race_eth_idx"] == i[0]) & 
                (vis_fig2_df["age_bin"] == i[1])]["person_id"].values[0]
        person_counts = np.append(person_counts, count)
    small_sample = person_counts < 20

    sns.set_theme(style="ticks")
    sns.set(font_scale = 2)
    sns.set(rc={'figure.figsize':(18,12)})

    # Draw a nested barplot by species and sex
    g = sns.FacetGrid(vis_fig2_df, col='race_eth_idx',
                      height=4, margin_titles=False,
                      sharey=True,
                      despine = False
                      #col_order=['Poor', 'Near poor', 'Not poor']
                     )
    g.set(yticks=y_ticks)
    g.set(ylim=[0, y_ticks[-1]])
    
    g.map_dataframe(sns.barplot, 
        y="percent",x="age_bin", order=dis_order,
        orient='v', errorbar=None,
        palette="Accent", alpha=1)

    # do low sample hatching
    hatch_color = [0,0,0,.3]
    all_bars = []    
    for ax in g.axes.flat:
        bars = ax.get_children()[:4]
        all_bars = np.append(all_bars, bars)
    for i, b in enumerate(all_bars):
        if small_sample[i]:
            #b = b.set(height=1,
            #         color="Red")
            b.set_hatch("\\")
            b.set_edgecolor(hatch_color)

    g.set_titles(col_template="{col_name}", row_template="{row_name}", fontdict={'fontsize': 24, 'fontweight':'bold'})

    # hardcode race hlines
    xmax_vals = [.23, .48, .73, .98]
    ann_vals = [-.2, .75, 1.74, 2.7]
    # get n=
    nine_n_eq = [sum(person_counts[i:i+4]) for i in np.arange(0,len(person_counts),4)]
    # write titles
    g.set(xticklabels=[])
    title_idx = 0
    for col_key, ax in g.axes_dict.items():
        
        ax.set_title(short_race_dict[col_key] + f" N=({int(nine_n_eq[title_idx])})", size=14)
        #############
        for i, l in enumerate(age_group_vals[title_idx]):
            patches = [p for p in ax.patches]
            
            ax.axhline(y = l,
                       xmin = xmax_vals[i] - .205,
                       xmax = xmax_vals[i],
                   color = 'black', linestyle='--')
            ax.annotate("\u0394" + " " + f'{l-patches[i].get_height():.2f}'+"%",
                           (ann_vals[i]-.15, l-annotation_offset), size=12)
        title_idx += 1

    g.despine(right=True)
    g.set_axis_labels("", "%")

    g.fig.subplots_adjust(top=0.9)


    patches = [mp.Patch(color=v, label=k) for k,v in name_to_color.items()]

    plt.subplots_adjust(hspace=0.2, wspace=0.1)

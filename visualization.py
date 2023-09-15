######################################################################################################
def plot_fig_3_left(inter_df, sense, age_group_vals, y_ticks, annotation_offset, delta_ann):
    """
    Visualize (highly structured, see below) ses_df across the intersection of
    blindness/deafness, sex, poverty status, and education level, with plot annotation.

    inter_df is a grouped df with unique person count, group denominator in AoURP EHR cohrt, and percent
    for each row. Rows specified by unique combo of race_eth, condition, education_group, and poverty columns.
    """
    
    dis_order = ['Less than a high school degree or equivalent',
            'Highest Grade: Twelve Or GED',
            'Highest Grade: College One to Three',
            'College graduate or advanced degree']
    inc_df = inter_df[inter_df['answer'].isin(dis_order)]
    vis_fig2_df = inter_df[inter_df['Cond_Category_R1'] == sense]


    tup_list = []
    for r in ['Female', 'Male']:
        for s in ['Poor', 'Near poor', 'Not poor']:
            for a in dis_order:
                tup_list.append([r, s, a])

    person_counts = []
    for i in tup_list:
        count = vis_fig2_df[(vis_fig2_df["sex_at_birth"] == i[0]) & 
                (vis_fig2_df["status"] == i[1]) &
                (vis_fig2_df["answer"] == i[2])]["person_id"].values[0]
        person_counts = np.append(person_counts, count)
    small_sample = person_counts < 20

    sns.set_theme(style="whitegrid")
    sns.set(font_scale = 2)
    sns.set(rc={'figure.figsize':(18,12)})

    # Draw a nested barplot by species and sex
    g = sns.FacetGrid(vis_fig2_df, col='status', row='sex_at_birth',
                      height=4, aspect=1, margin_titles=False,
                      sharey=True, #'row'
                      col_order=['Poor', 'Near poor', 'Not poor'])
    
    g.map_dataframe(sns.barplot, 
        y="percent",x="answer", order=dis_order,
        orient='v', errorbar=None,
        palette="colorblind", alpha=.8)
    
    g.set(yticks=y_ticks)
    g.set(ylim=[0, y_ticks[-1]])

    # do low sample hatching
    hatch_color = [0,0,0,.3]
    all_bars = []    
    for ax in g.axes.flat:
        bars = ax.get_children()[:4]
        all_bars = np.append(all_bars, bars)
    for i, b in enumerate(all_bars):
        if small_sample[i]:
            b.set_alpha(0)
            
    g.set_titles(col_template="{col_name}", row_template="{row_name}", fontdict={'fontsize': 24, 'fontweight':'bold'})

    # hardcode
    xmax_vals = [.23, .48, .73, .98]
    ann_vals = [-.35, .65, 1.64, 2.65]
    # get n=
    nine_n_eq = [sum([p if p >= 20 else 0 for p in person_counts[i:i+4]]) for i in np.arange(0,len(person_counts),4)]
    # write titles
    g.set(xticklabels=[])
    title_idx = 0
    for (row_key, col_key), ax in g.axes_dict.items():
        ax.set_title(f"{row_key}"+", "+f"{col_key}"+f" N={int(nine_n_eq[title_idx])}", size=14)
        
        patches = [p for p in ax.patches]
        ########################
        if row_key == 'Female':
            inc_group_vals = age_group_vals[0][title_idx % 3]
        elif row_key == 'Male':
            inc_group_vals = age_group_vals[1][title_idx % 3]
        
        for i, l in enumerate(inc_group_vals):
            print(str(l-patches[i].get_height()),",", str(np.round(patches[i].get_height() / l,2)))
            
            if small_sample[4*title_idx + i]:
                continue
            
            ax.axhline(y = l,
                       xmin = xmax_vals[i] - .205,
                       xmax = xmax_vals[i],
                   color = 'black', linestyle='--')
            diff_sources = l-patches[i].get_height()
            if diff_sources > 0:
                arrow_char = u"$\u2193$"
            else:
                arrow_char = u"$\u2191$"
            
            ax.annotate(arrow_char + f'{diff_sources:.1f}'+"%",
                           (ann_vals[i]-.05, delta_ann), size=12)
        title_idx += 1


    g.despine(right=True)
    g.set_axis_labels("", "%")

    g.fig.subplots_adjust(top=0.9)

    #LEGEND
    name_to_color = {
        dis_order[0]:   sns.color_palette('colorblind')[0] + tuple([.8]),
        dis_order[1]:   sns.color_palette('colorblind')[1] + tuple([.8]),
        dis_order[2]:   sns.color_palette('colorblind')[2] + tuple([.8]),
        dis_order[3]:    sns.color_palette('colorblind')[3] + tuple([.8])
    }
    patches = [mp.Patch(color=v, label=k) for k,v in name_to_color.items()]

    plt.subplots_adjust(hspace=0.3, wspace=0.1)

# Call plot_fig_3_left
age_group_vals = np.array([
                            [np.zeros(4), np.zeros(4), np.zeros(4)],
                            [np.zeros(4), np.zeros(4), np.zeros(4)]
                          ]
                         )
answer_series = nihis_df.groupby(['sex_clean', 'pov_clean', 'edu_clean', 'vision_disability'])['WTFA_SA'].sum()
answer_series

for s, sex in enumerate(['Female', 'Male']):
    for i, race in enumerate(['Poor', 'Near Poor', 'Not Poor']):
        for j, age in enumerate(['Less than a high school degree or equivalent',
                'Highest Grade: Twelve Or GED',
                'Highest Grade: College One to Three',
                'College graduate or advanced degree']):
            age_group_vals[s, i,j] = np.round(100 * answer_series[sex][race][age]['Yes'] / (answer_series[sex][race][age]['Yes'] + answer_series[sex][race][age]['No']), 1)

plot_fig_3_left(inter_df, 'vision', age_group_vals, np.arange(0, 24, 2), 2, 15.3)

age_group_vals = np.array([
                            [np.zeros(4), np.zeros(4), np.zeros(4)],
                            [np.zeros(4), np.zeros(4), np.zeros(4)]
                          ]
                         )
answer_series = nihis_df.groupby(['sex_clean', 'pov_clean', 'edu_clean', 'hearing_disability'])['WTFA_SA'].sum()
answer_series

for s, sex in enumerate(['Female', 'Male']):
    for i, race in enumerate(['Poor', 'Near Poor', 'Not Poor']):
        for j, age in enumerate(['Less than a high school degree or equivalent',
                'Highest Grade: Twelve Or GED',
                'Highest Grade: College One to Three',
                'College graduate or advanced degree']):
            age_group_vals[s, i,j] = np.round(100 * answer_series[sex][race][age]['Yes'] / (answer_series[sex][race][age]['Yes'] + answer_series[sex][race][age]['No']), 1)

plot_fig_3_left(inter_df, 'hearing', age_group_vals, np.arange(0, 30, 5), 2, 14)

######################################################################################################

short_race_dict = {'Asian Not Hispanic or Latino' :'Asian',
                 'Black or African American Not Hispanic or Latino': 'Black/Afr. Am.',
                 'None Indicated Hispanic or Latino': 'Hispanic',
                 'White Not Hispanic or Latino': 'White',
                 'More than one population Not Hispanic or Latino': 'Multiracial'}

def plot_fig_3_right(inter_df, sense, age_group_vals, y_ticks, annotation_offset, delta_ann):
    """
    Visualize (highly structured, see below) inter_df across the intersection of
    blindness/deafness, sex, education, and specific three race-ethnicity groups, with plot annotation.

    inter_df is a grouped df with unique person count, group denominator in AoURP EHR cohrt, and percent
    for each row. Rows specified by unique combo of race_eth, condition, sex_at_birth, and education survey answer columns.
    """
    short_school_dict = {'Less than a high school degree or equivalent': '< HS',
                        'Highest Grade: Twelve Or GED': 'HS/GED',
                        'Highest Grade: College One to Three': 'College 1-3',
                        'College graduate or advanced degree': '≥ BA'}

    dis_order = ['Female', 'Male']
    inc_df = inter_df[inter_df['answer'].isin(dis_order)]
    vis_fig2_df = inter_df[inter_df['Cond_Category_R1'] == sense]


    tup_list = []
    for r in include_race_eth:
        for s in ['Less than a high school degree or equivalent',
                'Highest Grade: Twelve Or GED',
                'Highest Grade: College One to Three',
                'College graduate or advanced degree']:
            for a in dis_order:
                tup_list.append([r, s, a])

    person_counts = []
    for i in tup_list:
        count = vis_fig2_df[(vis_fig2_df["race_eth_idx"] == i[0]) & 
                (vis_fig2_df["answer"] == i[1]) &
                (vis_fig2_df["sex_at_birth"] == i[2])]["person_id"].values[0]
        person_counts = np.append(person_counts, count)
    small_sample = person_counts < 20

    sns.set_theme(style="whitegrid")
    sns.set(font_scale = 2)

    # Draw a nested barplot by species and sex
    g = sns.FacetGrid(vis_fig2_df, col='answer', row='race_eth_idx',
                      height=4, aspect=1, margin_titles=False,
                      sharey=True, #'row'
                      col_order=['Less than a high school degree or equivalent',
                                'Highest Grade: Twelve Or GED',
                                'Highest Grade: College One to Three',
                                'College graduate or advanced degree'])
    sex_color = ['#E1BE6A','#40B0A6']

    g.map_dataframe(sns.barplot, 
        y="percent",x="sex_at_birth", order=dis_order,
        orient='v', errorbar=None,
        palette=sns.color_palette(sex_color), alpha=.9)
    
    g.set(yticks=y_ticks)
    g.set(ylim=[0, y_ticks[-1]])

    # do low sample hatching
    hatch_color = [0,0,0,.3]
    all_bars = []    
    for ax in g.axes.flat:
        bars = ax.get_children()[:2]
        all_bars = np.append(all_bars, bars)
    for i, b in enumerate(all_bars):
        if small_sample[i]:
            b.set_hatch("\\")
            b.set_edgecolor(hatch_color)

    g.set_titles(col_template="{col_name}", row_template="{row_name}", fontdict={'fontsize': 24, 'fontweight':'bold'})

    # hardcode race hlines
    xmax_vals = [0.05, .55] #.73, .98]
    ann_vals = [-.18, .8 ]# 1.74, 2.63]

    # get n=
    nine_n_eq = [sum(person_counts[i:i+2]) for i in np.arange(0,len(person_counts),2)]
    # write titles
    g.set(xticklabels=[])
    title_idx = 0
    
    for (row_key, col_key), ax in g.axes_dict.items():
        
        patches = [p for p in ax.patches]
        ax.set_title(short_race_dict[row_key]+", "+f"{short_school_dict[col_key]}"+f" N={int(nine_n_eq[title_idx])}", size=14)
        ########################
        
        if row_key == 'Black or African American Not Hispanic or Latino':
            inc_group_vals = age_group_vals[0][title_idx % 4]
        elif row_key == 'None Indicated Hispanic or Latino':
            inc_group_vals = age_group_vals[1][title_idx % 4]
        elif row_key == 'White Not Hispanic or Latino':
            inc_group_vals = age_group_vals[2][title_idx % 4]
            
        for i, l in enumerate(inc_group_vals):
            print(str(l-patches[i].get_height()),",", str(np.round(patches[i].get_height() / l,2)))
            
            ax.axhline(y = l,
                       xmin = xmax_vals[i],
                       xmax = xmax_vals[i] + .405,
                   color = 'black', linestyle='--')
            diff_sources = l-patches[i].get_height()
            if diff_sources > 0:
                arrow_char = u"$\u2193$"
            else:
                arrow_char = u"$\u2191$"
            
            ax.annotate(arrow_char + f'{diff_sources:.2f}'+"%",
                           (ann_vals[i]-.1, delta_ann), size=15)
        title_idx += 1


    g.despine(right=True)
    g.set_axis_labels("", "%")
    g.fig.subplots_adjust(top=0.9)

    #LEGEND
    name_to_color = {
        dis_order[0]:   (225/256, 190/256, 106/256, 1),
        dis_order[1]:   (64/256, 176/256, 166/256, 1)
    }
    patches = [mp.Patch(color=v, label=k) for k,v in name_to_color.items()]

    plt.subplots_adjust(hspace=0.3, wspace=0.1)

# CALL plot_fig_age
cell_group_vals = np.array([
                            [np.zeros(2), np.zeros(2), np.zeros(2), np.zeros(2)],
                            [np.zeros(2), np.zeros(2), np.zeros(2), np.zeros(2)],
                            [np.zeros(2), np.zeros(2), np.zeros(2), np.zeros(2)]
                          ]
                         )
#working_nihis_df = nihis_df[nihis_df['age_clean'].isin(['18_44', '45_64'])]
answer_series = nihis_df.groupby(['race_eth_clean', 'edu_clean', 'sex_clean', 'vision_disability'])['WTFA_SA'].sum()

for h, race in enumerate(["Black/African American", "Hispanic", "White"]):
    for i, edu in enumerate(['Less than a high school degree or equivalent',
            'Highest Grade: Twelve Or GED',
            'Highest Grade: College One to Three',
            'College graduate or advanced degree']):
        for j, sex in enumerate(['Female', 'Male']):
            cell_group_vals[h,i,j] = np.round(100 * answer_series[race][edu][sex]['Yes'] / (answer_series[race][edu][sex]['Yes'] + answer_series[race][edu][sex]['No']), 1)

plot_fig_3_right(inter_df, 'vision', cell_group_vals, np.arange(0, 30, 3), 2, 19)

cell_group_vals = np.array([
                            [np.zeros(2), np.zeros(2), np.zeros(2), np.zeros(2)],
                            [np.zeros(2), np.zeros(2), np.zeros(2), np.zeros(2)],
                            [np.zeros(2), np.zeros(2), np.zeros(2), np.zeros(2)]
                          ]
                         )
#working_nihis_df = nihis_df[nihis_df['age_clean'].isin(['18_44', '45_64'])]
answer_series = nihis_df.groupby(['race_eth_clean', 'edu_clean', 'sex_clean', 'hearing_disability'])['WTFA_SA'].sum()

for h, race in enumerate(["Black/African American", "Hispanic", "White"]):
    for i, edu in enumerate(['Less than a high school degree or equivalent',
            'Highest Grade: Twelve Or GED',
            'Highest Grade: College One to Three',
            'College graduate or advanced degree']):
        for j, sex in enumerate(['Female', 'Male']):
            cell_group_vals[h,i,j] = np.round(100 * answer_series[race][edu][sex]['Yes'] / (answer_series[race][edu][sex]['Yes'] + answer_series[race][edu][sex]['No']), 1)

plot_fig_3_right(inter_df, 'hearing', cell_group_vals, np.arange(0, 36, 4), 2, 22)


######################################################################################################

def fig_four_cell_render(aourp_vals, nhis_vals, y_ticks, delta_ann, color_level):
    """
    (1/4) functions/helpers for plotting individual components of the "expanding levels of intersections figures".
    """
    # top level
    plt.rcParams["figure.figsize"] = [4, 3]
    
    df_data = aourp_vals.to_frame().reset_index()
    df_data.columns = ['group', 'prevalence']
    #return df_data
    g =  sns.barplot(data=df_data, y='prevalence', x='group',
                      color=color_level)
    ax = g.axes
    
    # hardcode race hlines
    xmax_vals = [0.04, .37, .7]
    ann_vals = [-.38, .7, 1.7]
    race_hatches = ["//", "o", "x"]
    
    
    for i, bar in enumerate([ax.patches][0]):
        print(nhis_vals[i], bar.get_height() / nhis_vals[i])
        
        ax.axhline(y = nhis_vals[i],
                   xmin = xmax_vals[i],
                   xmax = xmax_vals[i] + .275,
               color = 'black', linestyle='--')
        
        
        bar.set_hatch(race_hatches[i])
        
        diff_sources = nhis_vals[i]-bar.get_height()
        
        if diff_sources > 0:
            arrow_char = u"$\u2193$"
        else:
            arrow_char = u"$\u2191$"

        ax.annotate(arrow_char + f'{diff_sources:.2f}'+"%",
                       (ann_vals[i]-.1, delta_ann), size=15)
        
    g.set(yticks=y_ticks)
    g.set(ylim=[0, y_ticks[-1]])
    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(rotation=90)
    plt.xticks([])
    plt.show()

def cell_configure(aourp_df, grouped_nihis, y_ticks, delta_ann, color): 
    """
    (2/4) functions/helpers for plotting individual components of the "expanding levels of intersections figures".
    """
    disab_df = aourp_df[aourp_df["answer"].isin(['College graduate or advanced degree',
         'Highest Grade: College One to Three',
         'Highest Grade: Twelve Or GED',
         'Less than a high school degree or equivalent'])]
    collapse_df = aourp_df.groupby(['race_eth_idx'])[['person_id', 'ehr_survey_race_eth_ses_denom']].sum()

def deep_fig_four_cell_render(aourp_vals, nhis_vals, y_ticks, delta_ann, color_level):
    """
    (3/4) functions/helpers for plotting individual components of the "expanding levels of intersections figures".
    """
    plt.rcParams["figure.figsize"] = [3, 3]
    
    df_data = aourp_vals.to_frame().reset_index()
    df_data.columns = ['group', 'prevalence']
    #return df_data
    g =  sns.barplot(data=df_data, y='prevalence', x='group',
                      color=color_level)
    ax = g.axes
    
    # hardcode race hlines
    xmax_vals = [0.04, .37, .7]
    ann_vals = [-.38, .7, 1.7]
    race_hatches = ["//", "o", "x"]
    
    
    for i, bar in enumerate([ax.patches][0]):
        print(nhis_vals[i], bar.get_height() / nhis_vals[i])
        
        ax.axhline(y = nhis_vals[i],
                   xmin = xmax_vals[i],
                   xmax = xmax_vals[i] + .275,
               color = 'black', linestyle='--')
        
        bar.set_hatch(race_hatches[i])
        
        diff_sources = nhis_vals[i]-bar.get_height()
        if diff_sources > 0:
            arrow_char = u"$\u2193$"
        else:
            arrow_char = u"$\u2191$"

        ax.annotate(arrow_char + f'{diff_sources:.1f}',
                       (ann_vals[i]-.1, delta_ann), size=15)
        
    g.set(yticks=y_ticks)
    g.set(ylim=[0, y_ticks[-1]])
    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(rotation=90)
    plt.xticks([])
    plt.show()

def deepest_layer_paramer(diab, sex, edu, edu_color, y_ticks, delta_ann):
    """
    (4/4) functions/helpers for plotting individual components of the "expanding levels of intersections figures".
    """
    aourp_df = wa_inter_df[wa_inter_df["Cond_Category_R1"] == diab]
    aourp_df = aourp_df[aourp_df['answer'] == edu]
    aourp_df = aourp_df[aourp_df['sex_at_birth'] == sex]
    ########################################
    grouped_nihis = working_nihis[working_nihis['edu_clean'] == edu]
    grouped_nihis = grouped_nihis[grouped_nihis['sex_clean'] == sex]
    grouped_nihis = grouped_nihis.groupby(['race_eth_clean', diab+"_disability"])['WTFA_SA'].sum()
    
    
    cell_configure(aourp_df, grouped_nihis,  y_ticks, delta_ann, edu_color)

# Call figure 4 functions per expanding layer
cell_group_vals = np.array([0, 0, 0])
    for h, race in enumerate(["Black/African American", "Hispanic", "White"]):
        cell_group_vals[h] = np.round(100 * grouped_nihis[race]['Yes'] / (grouped_nihis[race]['Yes'] + grouped_nihis[race]['No']), 1)

    fig_four_cell_render(aourp_vals, cell_group_vals, y_ticks, delta_ann, color)

# Example which spits out the top level group for all three race/eth among blind/low-vision.
# Re-call with different arguments for the 2*3 cells
aourp_df = wa_inter_df[wa_inter_df["Cond_Category_R1"] == 'vision']
grouped_nihis = working_nihis.groupby(['race_eth_clean', "vision_disability"])['WTFA_SA'].sum()

cell_configure(aourp_df, grouped_nihis, np.arange(0, 18, 2), 8, 'grey')

# Example for the 4*3 deepest layer plot outs
deepest_layer_paramer('vision', 'Female', 'Less than a high school degree or equivalent', sns.color_palette("colorblind")[0],
                     np.arange(-1,29,3), 19)

######################################################################################################
def plot_fig_age(ses_df, sense, age_group_vals, y_ticks, annotation_offset):
    """
    !unused in publication
    Visualize (highly structured, see below) ses_df across the intersection of
    blindness/deafness, age group, and a specific three race-ethnicity groups, with plot annotation.

    ses_df is a grouped df with unique person count, group denominator in AoURP EHR cohrt, and percent
    for each row. Rows specified by unique combo of race_eth, condition, age_group columns.
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

# CALL plot_fig_age
age_group_vals = np.array([np.zeros(4), np.zeros(4), np.zeros(4)])
answer_series = nihis_df.groupby(['race_eth_clean', 'age_clean', 'vision_disability'])['WTFA_SA'].sum()

for i, race in enumerate(["Black/African American", "Hispanic", "White"]):
    for j, age in enumerate(['18_44', '45_64', '65_74', '75_plus']):
        age_group_vals[i,j] = 100 * answer_series[race][age]['Yes'] / (answer_series[race][age]['Yes'] + answer_series[race][age]['No'])
        
plot_fig_age(ses_df, 'vision', age_group_vals, np.arange(0, 30, 5), 2)

age_group_vals = np.array([np.zeros(4), np.zeros(4), np.zeros(4)])
answer_series = nihis_df.groupby(['race_eth_clean', 'age_clean', 'hearing_disability'])['WTFA_SA'].sum()

for i, race in enumerate(["Black/African American", "Hispanic", "White"]):
    for j, age in enumerate(['18_44', '45_64', '65_74', '75_plus']):
        age_group_vals[i,j] = 100 * answer_series[race][age]['Yes'] / (answer_series[race][age]['Yes'] + answer_series[race][age]['No'])
        
plot_fig_age(ses_df, 'hearing', age_group_vals, np.arange(0, 60, 5), -2.5)

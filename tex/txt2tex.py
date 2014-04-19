#!/usr/bin/env python
import numpy as np
import sys,os

CLR = "For each column, the intensity of the color increases with the value"
SUF = "These values are generated at 650, 800 and 1000 MHz, at angular scales \\{0.4-1, 1-2, 2-3, 3-4, 600-3600\\} arcsec and are labeled {\\it resbin} \\{1, 2, 3, 4, 5\\} respectively. This is done for natural weighting at declinations -10, -30 and -50 degrees. %s."%CLR
CPT = {}
CPT["noise50k"] = "Noise (in $\\mu$Jy) for a 50kHz band after an 8hr synthesis with a 60s integration for the differenr layouts at different angular scales. %s"%SUF
CPT["noise50"] = "Noise (in $\\mu$Jy) for a 50MHz band after an 8hr synthesis with a 60s integration for the differenr layouts at different angular scales. %s"%SUF
CPT["noise166"] = "Noise (in $\\mu$Jy) for a 166MHz band after an 8hr synthesis with a 60s integration for the different layouts at different angular scales. %s"%SUF
CPT["snr10"] = "SNR after 8 hours relative to a 10$\\mu$Jy source at 1000Hz (166 MHz band) with a spectral index of -0.7 for the different layouts. %s"%SUF

CPT["snravg"] = "SNR after 8 hours relative to a 10$\\mu$Jy source at 1000Hz (166 MHz band) with a spectral index of -0.7 averaged over 650,800 and 1000MHz, for the different layouts at different angular scales. These values are generated for angular scales \\{0.4-1, 1-2, 2-3, 3-4, 600-3600\\} arcsec and are labeled {\\it resbin} \\{1, 2, 3, 4, 5\\} respectively. This is done for natural weighting at declinations -10, -30 and -50 degrees. %s."%CLR

CPT["hours"] = "The hours required to reach a mean SNR of 10 (average over 650,800 and 1000MHz), relative to a 10$\\mu$Jy source at 1000MHz with a spectral index of -0.7 for the different layouts at different angular scales. These values are generated for angular scales \\{0.4-1, 1-2, 2-3, 3-4, 600-3600\\} arcsec and are labeled {\\it resbin} \\{1, 2, 3, 4, 5\\} respectively. This is done for natural weighting at declinations -10, -30 and -50 degrees. %s."%CLR

CPT["speed"] = "Relative (w.r.t SKASUR) survey speeds for the different layouts, calculated using the FOV (using PAF FOV for SKASUR) values given in the SRD \\cite{srd} and the values in table \\ref{tab:hours-%s}. These values are generated for angular scales \\{0.4-1, 1-2, 2-3, 3-4, 600-3600\\} arcsec and are labeled {\\it resbin} \\{1, 2, 3, 4, 5\\} respectively at declenations -10, -30 and -50 degrees. %s."%(sys.argv[-1],CLR)

CPT["speed_avg"] = "Relative (w.r.t SKASUR) average survey speeds for the different layouts, calculated using the FOV (PAF FOV for SKASUR) values given in the SRD \\cite{srd} and the values in table \\ref{tab:snr10-%s}. These values are generated for angular scales \\{0.4-1, 1-2, 2-3, 3-4, 600-3600\\} arcsec and are labeled {\\it resbin} \\{1, 2, 3, 4, 5\\} respectively. This is done for natural weighting at declenations -10, -30 and -50 degrees. %s."%(sys.argv[-1],CLR)

CPT["psf_sym"] = "PSF symmetry (see \\autoref{sec:exp})  for the different layouts at different angular scales. These values are generated at 650, 800 and 1000MHz, for angular scales \\{0.4-1, 1-2, 2-3, 3-4, 600-3600\\} arcsec and are labeled {\\it resbin} \\{1, 2, 3, 4, 5\\} respectively. This is done for natural weighting at declinations -10, -30 and -50 degrees. %s."%CLR

CPT["psf_mean"] = "FWHM PSF sizes (in arcseconds) for the different layouts at different angular scales. These values are generated at 650, 800 and 1000MHz, for angular scales \\{0.4-1, 1-2, 2-3, 3-4, 600-3600\\} arcsec and are labeled {\\it resbin} \\{1, 2, 3, 4, 5\\} respectively. This is done for natural weighting at declinations -10, -30 and -50 degrees. %s."%CLR

def select_color(c,v,color):
   fct = .6
   val = c *70 + 30
   return "%.2f \\cellcolor{%s!%.2f}"%(v,color,val*fct) if v<1e2 else "%.4g \\cellcolor{%s!%.2f}"%(v,color,val*fct)

def color(data):
    new = np.ndarray([data.shape[0],data.shape[1]],dtype="S100")
    color = {'0':'blue','1':'red','2':'green','3':'orange','4':'purple','5':'blue','6':'red'}
    for i in range(data.shape[1]):
        min,max = float(data[:,i].min()),float(data[:,i].max())
        for j in range(data.shape[0]):
            cl = (data[j,i]-min)/(max-min) if data[j,i]!=min else 0
            new[j,i] = select_color(cl,data[j,i],color[repr(i)])
    return new

def caption(metric,cpt=CPT):
  """Returns caption for a given metric"""
  return "\\caption{%s}"%(cpt[metric])

if __name__=="__main__":

  std = open(sys.argv[1])
  hdr = std.readline()
  std.close()
  hdr = hdr[2:-1]
  names = hdr.split()
  dtype = ["float64"]*len(names)
  dtype[0],dtype[5],dtype[7] = ["S30"]*3
  decs,ndecs = "-10 -30 -50".split(),3
  #weights = "natural weighting,robust-2 weighting ,robust-2 weighting with a 1 arcsec Gaussian taper".split(",")
  weights,nwi = ["natural weighting"],1
  freqs,nfreqs = [650,800,1000],3
  decsWeights = {}
  for d in decs:
    for j,w in enumerate(weights):
       decsWeights["%s:%d"%(d,j)] = "DEC=%s, %s"%(d,w)
  lays,nlays = ["SKA1REF2","SKA1W9-12A72B120","SKA1W9-0A72B120","SKASUR"],4
  Stats = np.genfromtxt(sys.argv[1],names=names,dtype=dtype)
  stats = Stats[np.argsort(Stats,order=["dec","widx","lo0","freq","ridx"])]
  resbins = 5
  STATS = {}
  metrics = names[9:]
  for n in range(nlays*ndecs*nwi):
    start,end = n*resbins*nfreqs,(n+1)*resbins*nfreqs
    res = stats[start:end]
    s = {}
    for freq in range(nfreqs):
      tmp = "%d:%s:%d"%(res["dec"][0],res["lo0"][0],res["widx"][0])
     # print tmp,"\n------------------"
      for metric in metrics:
       vals = res[metric]
       s[metric] = vals
      STATS[tmp] = s
  METRIC = {}
  for wi in "0 1 2".split():
   for dec in "-50 -30 -10".split():
    LAY = {}
    for item in STATS.keys():
      if item.endswith(wi):
        if item.startswith(dec):
            for metric in metrics:
                for lay in lays:
                    key = "%s:%s"%(dec,wi)
                    if item.split(":")[1]==lay:
                        LAY.setdefault(lay,[]).append([metric,STATS[item][metric]])
                METRIC[key] = LAY
  def get_table(met,lays):
   final = {}
   for item in METRIC.keys():
    data = []
    for lay in lays:
        for i in METRIC[item][lay]:
            if i[0]==met: 
                data.append(i[1].tolist())
    final[item] = [lays,np.array(data)]
   return final

  exclude = ["flux10","relnoise","noise50_ref2","psf_xyBPA","psf_area"]
  # only include these layouts in the write up
# lays = ["SKA1REF2","SKA1W9-12A54B90","SKA1W9-12A60B100","SKA1W9-0A60B100","SKA1W9-12A72B120","SKA1W9-12A80B133"]
# nlays = len(lays)
  for metric in metrics:
   if metric not in exclude:
    final = get_table(metric,lays)
    try: texname = "%s-%s.tex"%(metric,sys.argv[2])
    except IndexError: texname = "%s.tex"%(metric) 
    texfile = open(texname,"w")
    texfile.write("% Auto generated table\n \\begin{table}[!htp]\n \\tiny{\n")
    ncols = resbins*nfreqs + 1
    nrows = nlays
    fmt =  repr(["$(c%d)s"%d for d in range(ncols)]).strip("[]").replace("'","").replace(","," &").replace("$","%")
    cols = ["c%d"%d for d in range(ncols)]
    keys = final.keys()
    keys.sort()
    if metric not in ["hours","snravg","speed","speed_avg"]:
     for key in keys:
      x = final[key][1]
      typ = ["S30"]*ncols
      dtype = [item for item in zip(cols,typ)]
      s = np.ndarray([x.shape[0],x.shape[1]+1],dtype="S100")
      s[:,0] = lays
      s[:,1:(resbins+1)] = color(x[:,:resbins])
      s[:,(resbins+1):(2*resbins+1)] = color(x[:,resbins:(2*resbins)])
      s[:,(2*resbins+1):(3*resbins+1)] = color(x[:,(2*resbins):(3*resbins)])
      top = "\\subfloat[%s]{\\begin{tabular}{|lccccc||ccccc||ccccc|} \n \\tabularnewline \\cline{2-16} \\multicolumn{1}{c}{ } & \\multicolumn{5}{|c}{650MHz}  & \\multicolumn{5}{c}{800MHz}  & \\multicolumn{5}{c|}{1000MHz} \\tabularnewline \\cline{1-16} \n resbin  &1 & 2 & 3 & 4 & 5 & 1 & 2 & 3 & 4 & 5 & 1 & 2 & 3 & 4 & 5 \\tabularnewline \\hline\n"%(decsWeights[key]) 
      texfile.write(top)
      for row in range(nrows):
       for i,col in enumerate(cols): 
         locals()[col] = s[row,i]
       texfile.write(fmt%locals()+"%s \\hline \n"%('\\tabularnewline' if (nrows-row) == 1 else '\\\\'))
       #print "-------------------------------------------\n",fmt%locals()
      texfile.write("\\end{tabular}}\\hfil \n")
    else :
      print metric
      ncols = resbins + 1
      cols = ["c%d"%d for d in range(ncols)]
      typ = ["S30"]*ncols
      dtype = [item for item in zip(cols,typ)]
      s = np.ndarray([nlays,ncols],dtype="S100")
      fmt1 =  repr(["$(c%d)s"%d for d in range(ncols)]).strip("[]").replace("'","").replace(","," &").replace("$","%")
      s[:,0] = lays
      for i,key in enumerate(keys,start=0):
        s = np.ndarray([nlays,resbins+1],dtype="S100")
        s[:,0] = lays
        counter = range(0,ndecs*len(weights),ndecs)
        if i%nwi == 0:
          x = final[key][1]
          if metric.startswith('speed'):
           for j in range(resbins):
             x[:,j] = x[:,j]/x[-1,j]
          s[:,1:(resbins+1)] = color(x[:,:resbins])
          top = "\\subfloat[%s]{\\begin{tabular}{|lccccc|} \\hline \n resbin & 1 & 2 & 3 & 4 & 5 \\tabularnewline \\hline\n"%(decsWeights[key])
          texfile.write(top)
          for row in range(nrows):
            for i,col in enumerate(cols): 
        #      print i,col,s[row,i]
              locals()[col] = s[row,i]
            texfile.write(fmt1%locals()+"%s \\hline \n"%('\\tabularnewline' if (nrows-row) == 1 else '\\\\'))
            #print "-------------------------------------------\n",fmt1%locals()
          texfile.write("\\end{tabular}}\\hfil \n")
    texfile.write("\n"+caption(metric)+"\\label{tab:%s-%s}"%(metric,sys.argv[2]))
    texfile.write("}\n \\end{table}")
    texfile.close()

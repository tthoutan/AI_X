

library(caret)
library(e1071)



#데이터 불러오기

df_match1 <- read.csv("match_info_partition1_8.csv")
df_match2 <- read.csv("match_info_partition1_23.csv")
df_match3 <- read.csv("match_info_partition2_23.csv")
df_match4 <- read.csv("match_info_partition3_23.csv")
df_match5 <- read.csv("match_info_partition4_22.csv")

df_match <- rbind(df_match1[,-1],df_match2[,-1],df_match3[,-1],df_match4[,-1],df_match5[,-1])

df_match$champ1 <-factor(df_match$champ1)
df_match$champ2 <-factor(df_match$champ2)
df_match$champ3 <-factor(df_match$champ3)
df_match$champ4 <-factor(df_match$champ4)
df_match$champ5 <-factor(df_match$champ5) 
df_match$win <- factor(df_match$win)


df_match$champ1 <- relevel(df_match$champ1,ref="1")
df_match$champ2 <- relevel(df_match$champ2,ref="1")
df_match$champ3 <- relevel(df_match$champ3,ref="1")
df_match$champ4 <- relevel(df_match$champ4,ref="1")
df_match$champ5 <- relevel(df_match$champ5,ref="1")
df_match$win <- relevel(df_match$win,ref="1")

summary(df_match$champ1)
levels(df_match$champ1)


#train/valid

set.seed(11)

ti <- sample(c(1:dim(df_match)[1]),dim(df_match)[1]*0.8)
train.df <- df_match[ti,]
valid.df <- df_match[-ti,]


win.nb <- naiveBayes(win~.,data=train.df)

pred.pb <- predict(win.nb,newdata = valid.df, type="raw")
pred.class <-predict(win.nb,newdata = valid.df)
confusionMatrix(pred.class,valid.df$win)


#실제 사용 / y1,y2,y3,y4에 아군 챔피언을, y5에 자기 챔피언을  영문으로 선언

#예시

df.champ <- read.csv("champ_info.csv")
head(df.champ)

y1 <- "Zac"
y2 <- "Yasuo"
y3 <- "Ashe"
y4 <- "Nautilus"
y5 <- "Garen"

#5개 다 정해진 경우

champ.function <- function(x1,x2,x3,x4,x5){
  
  for(i in 1:146){
    
    if(df.champ[i,3]==x1){champ1 <- df.champ[i,2]}
    if(df.champ[i,3]==x2){champ2 <- df.champ[i,2]}
    if(df.champ[i,3]==x3){champ3 <- df.champ[i,2]}
    if(df.champ[i,3]==x4){champ4 <- df.champ[i,2]}
    if(df.champ[i,3]==x5){champ5 <- df.champ[i,2]}
  
  }
  
  temp <- data.frame(champ1,champ2,champ3,champ4,champ5)
  
  for(i in 1:5){
    temp[,i] <- factor(temp[,i])
  }
  prob <- predict(win.nb, newdata = temp,type='raw')
  return(prob)
  
}


 champ.function(y1,y2,y3,y4,y5)


#아군 4명이 정해졌을 때 추천



recommand.function <- function(x1,x2,x3,x4){
  
  for(i in 1:146){
    
    if(df.champ[i,3]==x1){champ1 <- df.champ[i,2]}
    if(df.champ[i,3]==x2){champ2 <- df.champ[i,2]}
    if(df.champ[i,3]==x3){champ3 <- df.champ[i,2]}
    if(df.champ[i,3]==x4){champ4 <- df.champ[i,2]}
    
  }
  
  list <- df.champ$key
  list2 <- setdiff(list,champ1)
  list2 <- setdiff(list2,champ2)
  list2 <- setdiff(list2,champ3)
  list2 <- setdiff(list2,champ4)
  
  list3 <- df.champ$name
  list3 <- setdiff(list3,x1)
  list3 <- setdiff(list3,x2)
  list3 <- setdiff(list3,x3)
  list3 <- setdiff(list3,x4)
  
  tmp <- data.frame(champ1=c(1:142),champ2=c(1:142),champ3=c(1:142),champ4=c(1:142),champ5=c(1:142))
  for(i in 1:142){
    tmp$champ1[i] <- champ1
    tmp$champ2[i] <- champ2
    tmp$champ3[i] <- champ3
    tmp$champ4[i] <- champ4
    tmp$champ5[i] <- list2[i]
  }
  for(i in 1:5){
    tmp[,i] <- factor(tmp[,i])
  }
  
  for(i in 1:4){
    
  }
  
  
  prob <- predict(win.nb,newdata = tmp,type='raw')
  tmp2 <- data.frame(tmp$champ5,name=list3,prob[,1])
  tmp2 <- tmp2[c(order(-tmp2$prob)),]
  return(head(tmp2,10))
  
}



recommand.function(y1,y2,y3,y4)

# 10분위 향상 차트


lift <- lift(valid.df$win~pred.pb[,1])
xyplot(lift,plot="gain")


#번외 로지스틱 회귀(안돌아가서 데이터 10%만쓴걸로 다시)



lm.fit <- glm(win~.,data=train.df,family = binomial)
lm.fit
pred.lm <- predict(lm.fit,newdata=valid.df)
confusionMatrix(pred.lm,valid.df$win)



new<- sample(c(1:dim(df_match)[1]),dim(df_match)[1]*0.1)
new.df <- df_match[new,]

nt <- sample(c(1:dim(new.df)[1]),dim(new.df)[1]*0.8)
nt.df <- new.df[nt,]
nv.df <- new.df[-nt,]


lm.fit2 <- glm(win~.,data=nt.df,family = binomial)
lm.fit2
head(nv.df)
pred.lm2 <- predict(lm.fit2,newdata=nv.df,type="response")
pred.lm2 <- factor(ifelse(pred.lm2>0.5,1,0))
confusionMatrix(pred.lm2,nv.df$win)
head(pred.lm2)




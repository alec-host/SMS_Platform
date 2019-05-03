#!/usr/bin/python
"""
developer skype: alec_host
"""

"""
sms action list.
"""
TPL_BALANCE      = ["Dear {0},\nyour current balance : {1}\n{2}","Hi {0},\nyour current balance : {1}\n{2}"]
TPL_WITHDRAW     = ["Dear {0},\nyou have successfuly withdrawn: {1} from your account.\nCurrent balance: {2}.\n{3}","Hi {0},\nyou have successfuly withdrawn: {1} from your account.\nYour current balance: {2}.\n{3}"]
TPL_WITHDRAW_MIN = ["Dear {0},\nthe request has failed. Minimum amount that can be withdrawn : {1}.\n{2}","Hi {0},\n the request has failed. Minimum amount that can be withdrawn : {1}.\n{2}"]
TPL_WITHDRAW_MAX = ["Dear {0},\nthe request has failed. Maximum amount that can be withdrawn per day : {1}.\n{2}","Hi {0},\n the request has failed. Maximum amount that can be withdrawn per day : {1}.\n{2}"]
TPL_INSUFFICIENT = ["Dear {0},\nyou have insufficient balance to complete this request.\nCurrent balance : {1}.\n{2}","Hi {0}, you have insufficient balance to complete this action.\nCurrent balance : {1}.\n{2}"]
TPL_REGISTRATION = ["Dear User,\nWelcome to BETVANTAGE, your account has been created.\nKindly top up your account via MPESA Pay bill number: {0}.\n{1}","Hi User, welcome to BETVANTAGE, your account has been created. Kindly top up your account via MPESA Pay bill number: {0}.\n{1}"]
TPL_TOP_UP       = ["Dear {0},\nyour account has been topped up. Current balance: {1}.\n{2}","Hi {0},\nyour account has been topped up. Current balance: {1}.\n{2}"]
TPL_STOP         = ["Dear {0},\nyour request has been received. You will not receive anymore promotional SMS notifications.\n{1}","Hi {0},\nyour request has been received. You will not receive anymore promotional SMS notifications.\n{1}"]

TPL_SUCCESS_BET  = ["Dear {0},\nyou has successfully placed your bet :\n{1}.\n{2}","Hi {0},\nyou has successfully placed your bet :\n{1}.\n{2}"]
TPL_INVALID_BET  = ["Dear {0},\ninvalid bet, kindly confirm whether the stake details are correct :\n{1}.","Hi {0},\nkindly confirm whether the stake details are correct :\n{1}."]

TPL_STAKE_AMOUNT = ["Dear {0},\ninvalid bet, minimum amount that can be staked : {1}.\n{2}","Hi {0},\ninvalid bet, minimum amount that can be staked : {1}.\n{2}."]
